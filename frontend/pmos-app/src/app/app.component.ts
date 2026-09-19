import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  template: `
    <app-navbar></app-navbar>
    <main class="main-content">
      <router-outlet></router-outlet>
    </main>
    <footer class="app-footer">
      <p>&copy; 2026 PMOS Health Assistant Project. All rights reserved.</p>
    </footer>
  `,
  styles: [`
    :host {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .main-content {
      flex: 1;
      background-color: #f8fafc;
      min-height: calc(100vh - 140px);
    }
    .app-footer {
      text-align: center;
      padding: 1.5rem;
      background-color: #0f172a;
      color: #94a3b8;
      font-size: 0.9rem;
      margin-top: auto;
    }
  `]
})
export class AppComponent {}

