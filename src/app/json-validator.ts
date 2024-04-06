import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function jsonValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    try {
      JSON.parse(control.value);
      return null; // JSON is valid
    } catch (error) {
      return { invalidJson: true }; // JSON is invalid
    }
  };
}
