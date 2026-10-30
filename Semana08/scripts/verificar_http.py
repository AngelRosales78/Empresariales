"""Cliente HTTP externo reproducible: usa requests y un servidor real, no APIClient."""
import argparse
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import requests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8000')
    parser.add_argument('--output', default='docs/evidencias/http.json')
    args = parser.parse_args()
    token = os.environ.get('QUIZ_TOKEN')
    if not token:
        parser.error('Define QUIZ_TOKEN con el token de un usuario staff.')
    session = requests.Session()
    session.headers.update({'Authorization': f'Token {token}', 'Accept': 'application/json'})
    records = []
    def call(method, path, expected, body=None):
        response = session.request(method, args.url.rstrip('/') + path, json=body, timeout=15)
        data = response.json() if response.content else None
        records.append({'method': method, 'path': path, 'body': body, 'status': response.status_code, 'response': data})
        assert response.status_code == expected, records[-1]
        return data
    # Solo se eliminan registros creados por este recorrido.
    exam = call('POST', '/api/exams/', 201, {'title': 'Verificación HTTP Semana08'})
    eid = exam['id']
    body = {'exam': eid, 'text': '¿Qué es REST?', 'choices': [
        {'text': 'Estilo de arquitectura', 'is_correct': True},
        {'text': 'Lenguaje', 'is_correct': False}]}
    q = call('POST', '/api/questions/', 201, body)
    qid = q['id']
    choice = call('POST', '/api/choices/', 201, {'question': qid, 'text': 'Distractor adicional', 'is_correct': False})
    for resource, identifier, update in [('exams', eid, {'title': 'Examen HTTP modificado'}),
                                          ('questions', qid, {'text': '¿Qué significa REST?'}),
                                          ('choices', choice['id'], {'text': 'Distractor modificado'})]:
        assert 'results' in call('GET', f'/api/{resource}/', 200)
        call('GET', f'/api/{resource}/{identifier}/', 200)
        changed = call('PATCH', f'/api/{resource}/{identifier}/', 200, update)
        assert all(changed[k] == v for k, v in update.items())
    missing = {k: v for k, v in body.items() if k != 'text'}
    call('POST', '/api/questions/', 400, missing)
    call('POST', '/api/questions/', 400, {**body, 'exam': 'no-es-un-numero'})
    wrong = {**body, 'choices': [{'text': 'a', 'is_correct': True}, {'text': 'b', 'is_correct': True}]}
    call('POST', '/api/questions/', 400, wrong)
    call('POST', '/api/questions/', 400, {**body, 'choices': [{'text': 'a'}, {'text': 'b'}]})
    filtered = call('GET', f'/api/questions/?exam={eid}', 200)
    assert all(item['exam'] == eid for item in filtered['results'])
    searched = call('GET', f'/api/questions/?exam={eid}&search=significa', 200)
    assert searched['count'] == 1
    # Generar seis preguntas adicionales garantiza una segunda página incluso en una BD vacía.
    for number in range(6):
        call('POST', '/api/questions/', 201, {**body, 'text': f'Paginación HTTP {number}'})
    page1 = call('GET', f'/api/questions/?exam={eid}', 200)
    page2 = call('GET', f'/api/questions/?exam={eid}&page=2', 200)
    assert (page1['count'], len(page1['results']), len(page2['results'])) == (7, 5, 2)
    assert page1['next'] and page2['previous'] and page2['next'] is None
    for resource, identifier in [('choices', choice['id']), ('questions', qid), ('exams', eid)]:
        call('DELETE', f'/api/{resource}/{identifier}/', 204)
        call('GET', f'/api/{resource}/{identifier}/', 404)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'date_utc': datetime.now(timezone.utc).isoformat(), 'base_url': args.url,
                                  'requests': records}, ensure_ascii=False, indent=2), encoding='utf8')
    print(f'{len(records)} peticiones verificadas. Evidencia: {output}')

if __name__ == '__main__':
    main()
