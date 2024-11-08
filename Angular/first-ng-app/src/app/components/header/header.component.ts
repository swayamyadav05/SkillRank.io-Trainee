import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent {
  @Input() showLogoutButton: boolean = false;
  @Output() onLogout = new EventEmitter<void>();

  constructor(private router: Router) {}

  navigateToHome(): void {
    this.router.navigate(['/home']);
  }

  handleKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.navigateToHome();
    }
  }

  logout(): void {
    this.onLogout.emit();
  }
}
