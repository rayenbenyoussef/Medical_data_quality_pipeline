# Business Rules

## ED Visits

- each stay belongs to only one patient.
- patient can do multiple visits.
- arrival_date cannot be after discharge_date.
- stay_id is unique and not null.
- patient_status may be NULL.
- arrival transport must be one of:
  - ambulance
  - walk-in
  - unknown
- is_multi_diagnosed can be only yes or no
- disposition must be in:
  - admitted
  - home
  - other
  - left against medical advice
  - eloped
  - transfer
  - left without being seen

## vitalsigns

- acuity_level must be between 1 and 5.
- pain_level must be between 0 and 10.
- temperature must be between 12 and 43.
- heart_rate must be between 20 and 300.
- resp_rate must be between 4 and 60.
- o2_saturation must be between 50 and 100.
- systolic_bp must be between 30 and 320.
- diastolic_bp must be between 10 and 200.
- patient_status must be one of:
  - unable-to-assess
  - declined
  - asleep-or-resting
  - not-assessed
- card_rhythm must be one of:
  - Atrial Fibrillation
  - Sinus Rhythm
  - Paced Rhythm
  - Sinus Bradycardia
  - Sinus Tachycardia
  - unknown



## Patients

- patient_id is unique and not null.
- gender must be M or F.
- region must be one of:
  - europe
  - north-america
  - south-america
  - unknown
- race must be one of:
  - multiple
  - black/african
  - hispanic/latino
  - unknown
  - white

## Date

- date must be in this format yyyy-mm-dd.
- date must be realistic.

## Therapeutic classification group (ETC)

- etc code must be unique and not null.
- etc description may be null.

## Medications

- medication id must be unique.
- medication must have a name.
- Generic Sequence Number (GSN) may be null

## Hour

- hour must be in this format hh:mm .
- hour must be in 24-hour clock system.
- each part of the hours has a shift type.

## Chief complaint

- each Chief complaint has unique id.
- each Chief complaint belongs to one category.
- categories must be one of:
  - Abdominal
  - Cardiac
  - Respiratory
  - Neurological
  - Trauma
  - Psychiatric
  - Infectious
  - Metabolic
  - GI
  - Musculoskeletal
  - Urological
  - Vascular
  - Transfer
  - Other
- each patients on one visit can have multiple chief complaints.

## ICD

- icd id must be unique and not null.
- each icd code cant be null and can repeated.
- each icd code has its icd version only 9 or 10 cant be null.

## Diagnosis

- diagnosis_id is unique.
- every diagnosis references one stay_id.
- multiple diagnosis can be linked to one stay id

## Pyxis

- each dispensing happened has a unique id.
- can dispense multiple medications at the same operation.
- med event num show which medications dispensed together.

## Medrecon

- medrecon id must be unique.
- each stay id can have multiple medications taked by the patients before.
- recording date and hour must be the time that staff recorded the data.