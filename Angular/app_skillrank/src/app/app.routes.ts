import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    loadComponent: () => {
      return import('./home/home.component').then((m) => m.HomeComponent);
    },
  },
  {
    path: 'signup',
    loadComponent: () => {
      return import('./components/signup/signup.component').then(
        (m) => m.SignupComponent
      );
    },
  },
];
