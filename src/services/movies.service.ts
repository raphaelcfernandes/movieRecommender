import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Movie } from '../models/movie';
import { Observable } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable()
export class MoviesService {

  constructor(private http: HttpClient) { }

  public getAllMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>('http://localhost:8080/movies/getAllMovies');
  }

  public sendRecommendation(data): Observable<any> {
    return this.http.post('http://localhost:8080/movies/sendRecommendation', data, httpOptions);
  }
}
