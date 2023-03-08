import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TwitterResultatComponent } from './twitter-resultat.component';

describe('TwitterResultatComponent', () => {
  let component: TwitterResultatComponent;
  let fixture: ComponentFixture<TwitterResultatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TwitterResultatComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TwitterResultatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
