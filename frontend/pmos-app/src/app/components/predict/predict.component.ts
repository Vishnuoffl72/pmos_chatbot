import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, PredictResponse } from '../../services/api.service';

@Component({
  selector: 'app-predict',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './predict.component.html',
  styleUrl: './predict.component.css'
})
export class PredictComponent {
  formData = {
    age: null as number | null,
    weight: null as number | null,
    height: null as number | null,
    location: '',
    maritalStatus: '',
    firstCycleAge: null as number | null,
    cycleRegularity: '',
    pregnancyHistory: '',
    numChildren: 0,
    familyHistory: '',
    junkFoodFreq: '',
    chickenFreq: '',
    foodPattern: '',
    exerciseFreq: '',
    moodFrequency: '',
    physicalSymptoms: '',
    sleepHours: '',
    sleepIssues: {
      none: false,
      difficultyFalling: false,
      wakingFrequently: false,
      wakingEarly: false,
      snoring: false,
      fatigued: false
    }
  };

  isLoading = false;
  result: PredictResponse | null = null;
  errorMsg = '';

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  onSubmit() {
    this.isLoading = true;
    this.errorMsg = '';
    this.cdr.markForCheck();

    // Build sleep issues string (comma separated, matching dataset format)
    const issues: string[] = [];
    if (this.formData.sleepIssues.difficultyFalling) issues.push('Difficulty falling asleep');
    if (this.formData.sleepIssues.wakingFrequently) issues.push('Waking up frequently during the night');
    if (this.formData.sleepIssues.wakingEarly) issues.push('Waking up too early and unable to fall back asleep');
    if (this.formData.sleepIssues.snoring) issues.push('Severe snoring or waking up gasping for air');
    if (this.formData.sleepIssues.fatigued) issues.push('Feeling excessively tired or fatigued during the day');
    const sleepIssuesStr = issues.length > 0 ? issues.join(', ') : 'None of the above';

    // Map frontend form data to exact backend field names and values
    const payload = {
      Age: this.formData.age,
      Weight: this.formData.weight,
      Height: this.formData.height,
      age_of_first_period: this.formData.firstCycleAge,
      num_children: this.formData.numChildren,
      residential_location: this.formData.location,
      marital_status: this.formData.maritalStatus,
      menstrual_regularity: this.formData.cycleRegularity,
      family_history: this.formData.familyHistory,
      junk_food_freq: this.formData.junkFoodFreq,
      chicken_freq: this.formData.chickenFreq,
      food_pattern: this.formData.foodPattern,
      exercise_freq: this.formData.exerciseFreq,
      mood_issues: this.formData.moodFrequency,
      symptoms: this.formData.physicalSymptoms,
      sleep_hours: this.formData.sleepHours,
      sleep_issues: sleepIssuesStr,
      pregnancy_status: this.formData.pregnancyHistory
    };

    this.apiService.predictRisk(payload).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.result = res;
        this.cdr.markForCheck();
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMsg = 'Failed to assess risk. Please try again later.';
        console.error(err);
        this.cdr.markForCheck();
      }
    });
  }

  resetForm() {
    this.result = null;
    this.errorMsg = '';
    this.cdr.markForCheck();
  }

  getRiskColor(level: string): string {
    if (level === 'Low') return '#10b981';
    if (level === 'Moderate') return '#f59e0b';
    if (level === 'High') return '#ef4444';
    return '#0d9488';
  }
}
