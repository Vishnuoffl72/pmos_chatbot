import { Component, ElementRef, ViewChild, AfterViewChecked, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements AfterViewChecked {
  @ViewChild('scrollMe') private myScrollContainer!: ElementRef;

  messages: Message[] = [
    { text: "Hello! I'm your PMOS Health Assistant. I can answer questions about Polyendocrine Metabolic Ovarian Syndrome based on our research data. Try asking about symptoms, diet, exercise, or risk factors!", sender: 'bot' }
  ];

  userInput: string = '';
  isLoading: boolean = false;

  suggestions: string[] = [
    "What is PMOS?",
    "Common symptoms?",
    "How does diet affect PMOS?",
    "Exercise and PMOS",
    "Sleep and PMOS",
    "PMOS risk factors"
  ];

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      this.myScrollContainer.nativeElement.scrollTop = this.myScrollContainer.nativeElement.scrollHeight;
    } catch(err) { }
  }

  sendSuggestion(suggestion: string) {
    this.userInput = suggestion;
    this.sendMessage();
  }

  sendMessage() {
    if (!this.userInput.trim()) return;

    const userText = this.userInput.trim();
    this.messages.push({ text: userText, sender: 'user' });
    this.userInput = '';
    this.isLoading = true;
    this.cdr.markForCheck();

    this.apiService.sendMessage(userText).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.messages.push({ text: res.response, sender: 'bot' });
        this.cdr.markForCheck();
      },
      error: (err) => {
        this.isLoading = false;
        this.messages.push({ text: "Sorry, I'm having trouble connecting to the server. Please make sure the backend is running on port 8000.", sender: 'bot' });
        this.cdr.markForCheck();
      }
    });
  }
}
