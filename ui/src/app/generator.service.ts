import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class GeneratorService {

  private generatorUrl = 'http://127.0.0.1:5000/generate';
  private nGramUrl = 'http://127.0.0.1:5000/ngram';

  private nGram: number;
  private generateWords: string[];

  constructor(private http: HttpClient) {
    this.generateWords = new Array();
  }

  public generate(): void {
    this.http.get<string>(this.generatorUrl).pipe(
      catchError(this.handleError<string>('generate'))).subscribe(newWord => {
        // Set the scroll to the end
        this.generateWords.push(newWord);
      });
  }

  public nGramGet(): void {
    this.http.get<number>(this.nGramUrl).pipe(
      catchError(this.handleError<number>('getNGram'))).subscribe(newNGram => {
        this.nGram = newNGram;
      });
  }

  public nGramUpdate(nGram: number): void {
    this.http.put(this.nGramUrl, nGram, httpOptions).pipe(
      catchError(this.handleError<any>('putNGram'))).subscribe();
  }

  public get getNGram(): number {
    return this.nGram;
  }

  public get getGenerateWords(): string[] {
    const display = document.getElementById('display');
    display.scrollTop = display.scrollHeight;
    return this.generateWords;
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error); // log to console instead
      console.log(`${operation} failed: ${error.message}`);
      return of(result as T);
    };
  }

}
