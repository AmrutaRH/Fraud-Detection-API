import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { jsonValidator } from './json-validator'; 
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'Fraud-Detection-API';
  myForm: FormGroup;
result:boolean=false;
status:string="";
submissionError: string | null = null;

  constructor(private formBuilder: FormBuilder,
    private http: HttpClient
  ) {
    this.myForm = this.formBuilder.group({
      myInput: ['', [Validators.required, jsonValidator()]]
    });
  }

  ngOnInit() {
    
  }

  isFormValid(): boolean {
    return this.myForm.valid;
  }

  onSubmit() {
    if (this.myForm.valid) {
      const inputData = this.myForm.get('myInput')?.value;
      // Handle form submission
      this.http.get<any>('/api/Test/fraud_detect')
        .subscribe(
          response => {
            // Handle successful response
            console.log('Response:', response);
          },
          error => {
            // Handle errors
            console.error('Error:', error);
            this.submissionError = 'Error occurred while submitting the data.';
          }
        );
      this.status="not a Froud";
      this.result=true;
      console.log('Form submitted successfully');
    } else {
      this.status="a Froud"
      // Form is not valid, handle accordingly
    }
  }


}
