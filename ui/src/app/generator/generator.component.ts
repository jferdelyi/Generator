import { Component, OnInit } from '@angular/core';
import { GeneratorService } from '../generator.service';

@Component({
  selector: 'app-generator',
  templateUrl: './generator.component.html',
  styleUrls: ['./generator.component.scss']
})
export class GeneratorComponent implements OnInit {

  /**
   * Constructor
   * @param generatorService generator service injection
   */
  public constructor(private generatorService: GeneratorService) {
    // Nothing
  }

  /**
   * Init
   */
  public ngOnInit(): void {
    this.getNGram();
  }

  /**
   * Generate new word
   */
  public generate(): void {
    this.generatorService.generate();
  }

  /**
   * Get nGram
   */
  public nGramGet() {
    this.generatorService.nGramGet();
  }

  /**
   * Set nGram
   * @param nGram new nGram
   */
  public nGramUpdate(nGram: number): void {
    this.generatorService.nGramUpdate(nGram);
  }

  /**
   * Get nGram data from generator service
   */
  public getNGram(): number {
    return this.generatorService.getNGram;
  }

  /**
   * Get words data from generator service
   */
  public get generateWordsGet(): string[] {
    return this.generatorService.getGenerateWords;
  }
}
