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
  // Generator URL
  private generatorUrl = 'http://127.0.0.1:5000/generate';

  // N-GRAM URL
  private nGramUrl = 'http://127.0.0.1:5000/ngram';

  // N-GRAM
  private nGram: number;

  // Status of the connection
  private status: boolean = true;

  // Generated words
  private output: string[];

  /**
   * Generator service
   * @param http HTTP service
   */
  constructor(private http: HttpClient) {
    this.output = new Array();
  }

  /**
   * Generate a new word
   */
  public generate(): void {
    this.http.get<string>(this.generatorUrl).pipe(
      catchError(this.handleError<string>('generate'))).subscribe(newWord => {
        // Set the scroll to the end
        this.output.push(newWord);
      });
  }

  /**
   * Get N-GRAM
   */
  public nGramGet(): void {
    this.http.get<number>(this.nGramUrl).pipe(
      catchError(this.handleError<number>('getNGram'))).subscribe(newNGram => {
        this.nGram = newNGram;
      });
  }

  /**
   * Update N-GRAM, this function can be take long time
   * @param nGram new N-GRAM
   */
  public nGramUpdate(nGram: number): void {
    this.status = false;
    this.output.push("# Waiting for reconfiguration...")
    this.http.put(this.nGramUrl, nGram, httpOptions).pipe(
      catchError(this.handleError<any>('putNGram'))).subscribe(_ => {
        this.output[this.output.length -1] += "done"
        this.status = true;
      });
  }

  /**
   * Get N-GRAM
   */
  public get getNGram(): number {
    return this.nGram;
  }

  /**
   * Get connection status
   */
  public get getStatus(): boolean {
    return this.status;
  }

  /**
   * Get generated words
   */
  public get getOutput(): string[] {
    const display = document.getElementById('display');
    display.scrollTop = display.scrollHeight;
    return this.output;
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
