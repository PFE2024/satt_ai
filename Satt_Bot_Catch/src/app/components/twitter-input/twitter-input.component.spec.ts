import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TwitterInputComponent } from './twitter-input.component';

describe('TwitterInputComponent', () => {
  let component: TwitterInputComponent;
  let fixture: ComponentFixture<TwitterInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TwitterInputComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TwitterInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
