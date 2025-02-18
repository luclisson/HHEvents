import request from 'supertest';
import { jest } from '@jest/globals';
import app from './api.js';

// Mock external dependencies
jest.mock('./supabaseCon.js', () => ({
  fetchLatestDataWebsite: jest.fn(),
  insertDataFromScraperToDB: jest.fn(),
  fetchAllDataDb: jest.fn(),
}));

jest.mock('./scraperCon.js', () => ({
  loadJSON: jest.fn(),
}));

// Import mocked functions
import { fetchLatestDataWebsite, insertDataFromScraperToDB, fetchAllDataDb } from './supabaseCon.js';
import { loadJSON } from './scraperCon.js';

describe('API Routes', () => {
  test('GET / should return "application is running"', async () => {
    const response = await request(app).get('/');
    expect(response.status).toBe(200);
    expect(response.text).toBe('application is running');
  });

  test('GET /fetch/:id should return data for valid id', async () => {
    const mockData = { id: '123', name: 'Test Event' };
    fetchLatestDataWebsite.mockResolvedValue(mockData);

    const response = await request(app).get('/fetch/123');
    expect(response.status).toBe(200);
    expect(response.body).toEqual(mockData);
  });

  test('GET /insertData should insert data and return success message', async () => {
    loadJSON.mockReturnValue([{ title: 'Test Event', link: 'http://test.com' }]);
    insertDataFromScraperToDB.mockResolvedValue();

    const response = await request(app).get('/insertData');
    expect(response.status).toBe(200);
    expect(response.text).toBe('Successfully received data from the scraper and inserted it to the db');
  });

  test('GET /fetchData should return all data from DB', async () => {
    const mockData = [{ id: '1', name: 'Event 1' }, { id: '2', name: 'Event 2' }];
    fetchAllDataDb.mockResolvedValue(mockData);

    const response = await request(app).get('/fetchData');
    expect(response.status).toBe(200);
    expect(response.body).toEqual(mockData);
  });
});
