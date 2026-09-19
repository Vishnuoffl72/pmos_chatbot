import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PredictResponse {
  risk_score: number;
  risk_level: string;
  factors: string[];
  recommendations: string[];
}

export interface ChatResponse {
  response: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'https://pmos-chatbot-backend.onrender.com';

  constructor(private http: HttpClient) { }

  sendMessage(message: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.baseUrl}/api/chat`, { message });
  }

  predictRisk(data: any): Observable<PredictResponse> {
    return this.http.post<PredictResponse>(`${this.baseUrl}/api/predict`, data);
  }
}

