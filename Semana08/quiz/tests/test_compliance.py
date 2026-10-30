from rest_framework.test import APITestCase
from .helpers import seed, exam_id, valid_body
from quiz.models import Question


class ComplianceTests(APITestCase):
    def setUp(self):
        human, _ = seed()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {human}")

    def test_browsable_api_and_docs_render(self):
        for path in ("/api/exams/", "/api/questions/", "/api/choices/", "/api/docs/"):
            response = self.client.get(path, HTTP_ACCEPT="text/html")
            self.assertEqual(response.status_code, 200, path)
            self.assertIn(b"<html", response.content.lower())

    def test_second_page_has_remaining_questions(self):
        first = self.client.get("/api/questions/").json()
        second = self.client.get(first["next"]).json()
        self.assertEqual(len(second["results"]), 3)
        self.assertIsNone(second["next"])
        self.assertTrue({q["id"] for q in first["results"]}.isdisjoint(q["id"] for q in second["results"]))

    def test_choice_crud_and_integrity(self):
        question = Question.objects.first()
        response = self.client.post("/api/choices/", {"question": question.id, "text": "Distractor", "is_correct": False}, format="json")
        self.assertEqual(response.status_code, 201)
        path = f"/api/choices/{response.json()['id']}/"
        self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(self.client.patch(path, {"text": "Otro distractor"}, format="json").status_code, 200)
        self.assertEqual(self.client.patch(path, {"is_correct": True}, format="json").status_code, 400)
        self.assertEqual(self.client.delete(path).status_code, 204)
        correct = question.choices.get(is_correct=True)
        path = f"/api/choices/{correct.id}/"
        self.assertEqual(self.client.delete(path).status_code, 400)
        self.assertEqual(self.client.patch(path, {"is_correct": False}, format="json").status_code, 400)
        self.assertEqual(question.choices.filter(is_correct=True).count(), 1)

    def test_choice_requires_parent_and_cannot_move(self):
        self.assertEqual(self.client.post("/api/choices/", {"text": "Sin padre"}, format="json").status_code, 400)
        q1, q2 = list(Question.objects.all()[:2])
        path = f"/api/choices/{q1.choices.first().id}/"
        self.assertEqual(self.client.patch(path, {"question": q2.id}, format="json").status_code, 400)

    def test_nested_zero_two_and_missing_options_rejected(self):
        for flags in ((False, False), (True, True)):
            body = valid_body(exam_id())
            body["choices"] = [{"text": "a", "is_correct": flags[0]}, {"text": "b", "is_correct": flags[1]}]
            self.assertEqual(self.client.post("/api/questions/", body, format="json").status_code, 400)
        body.pop("choices")
        self.assertEqual(self.client.post("/api/questions/", body, format="json").status_code, 400)

    def test_replacing_options_is_atomic_and_preserves_readonly_fields(self):
        question = Question.objects.first()
        path = f"/api/questions/{question.id}/"
        old = list(question.choices.values_list("id", flat=True))
        self.assertEqual(self.client.patch(path, {"choices": []}, format="json").status_code, 400)
        self.assertEqual(list(question.choices.values_list("id", flat=True)), old)
        body = valid_body(exam_id())
        body["id"] = 99999
        response = self.client.patch(path, body, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], question.id)
        self.assertEqual(question.choices.count(), 3)

    def test_session_login_and_csrf(self):
        from django.contrib.auth.models import User
        from rest_framework.test import APIClient
        user = User.objects.get(username="profe")
        user.set_password("test-only")
        user.save()
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="profe", password="test-only"))
        self.assertEqual(client.get("/api/exams/", HTTP_ACCEPT="text/html").status_code, 200)
        self.assertEqual(client.post("/api/exams/", {"title": "Sin CSRF"}, format="json").status_code, 403)

    def test_patch_nested_options_require_text(self):
        question = Question.objects.first()
        response = self.client.patch(
            f"/api/questions/{question.id}/",
            {"choices": [{"is_correct": True}, {"is_correct": False}]},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(question.choices.count(), 4)

    def test_cannot_delete_last_distractor(self):
        from quiz.models import Choice
        question = Question.objects.create(exam_id=exam_id(), text="Dos opciones")
        Choice.objects.create(question=question, text="Correcta", is_correct=True)
        distractor = Choice.objects.create(question=question, text="Incorrecta", is_correct=False)
        self.assertEqual(self.client.delete(f"/api/choices/{distractor.id}/").status_code, 400)
        self.assertEqual(question.choices.count(), 2)
