import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NormativeComponent } from './normative.component';

@NgModule({
  declarations: [NormativeComponent],
  imports: [CommonModule, RouterModule],
  exports: [NormativeComponent]
})
export class NormativeModule { }
