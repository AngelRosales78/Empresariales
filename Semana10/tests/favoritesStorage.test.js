import { test, beforeEach, afterEach } from 'node:test'
import assert from 'node:assert/strict'
import { FAVORITES_KEY, readFavorites, saveFavorites } from '../src/utils/favoritesStorage.js'

let storage
beforeEach(() => {
  storage = new Map()
  globalThis.window = { localStorage: {
    getItem: (key) => storage.get(key) ?? null,
    setItem: (key, value) => storage.set(key, value),
  } }
})
afterEach(() => { delete globalThis.window })

test('a first visit starts with no favorites', () => {
  assert.deepEqual(readFavorites(['orbita']), [])
})

test('save and read preserve the list across app initializations', () => {
  assert.equal(saveFavorites(['orbita', 'medianoche']), true)
  assert.equal(storage.get(FAVORITES_KEY), '["orbita","medianoche"]')
  assert.deepEqual(readFavorites(['orbita', 'medianoche']), ['orbita', 'medianoche'])
})

test('old, duplicate and non-string identifiers are discarded', () => {
  storage.set(FAVORITES_KEY, '["orbita","orbita","removed",7,null]')
  assert.deepEqual(readFavorites(['orbita']), ['orbita'])
})

test('valid JSON with the wrong shape cannot break the app', () => {
  storage.set(FAVORITES_KEY, '{"orbita":true}')
  assert.deepEqual(readFavorites(['orbita']), [])
})

test('malformed saved JSON recovers with an empty list', (context) => {
  context.mock.method(console, 'warn', () => {})
  storage.set(FAVORITES_KEY, '{broken')
  assert.deepEqual(readFavorites(['orbita']), [])
})

test('a blocked browser storage read does not crash initialization', (context) => {
  context.mock.method(console, 'warn', () => {})
  window.localStorage.getItem = () => { throw new Error('Storage blocked') }
  assert.deepEqual(readFavorites(['orbita']), [])
})

test('a write failure is reported so the interface can explain it', (context) => {
  context.mock.method(console, 'warn', () => {})
  window.localStorage.setItem = () => { throw new Error('Quota exceeded') }
  assert.equal(saveFavorites(['orbita']), false)
})

test('removing every favorite persists an empty list', () => {
  saveFavorites(['orbita'])
  saveFavorites([])
  assert.deepEqual(readFavorites(['orbita']), [])
})
