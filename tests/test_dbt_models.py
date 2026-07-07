class TestDbtMarts:

    def test_dim_patients_exists_and_has_rows(self, real_reader):
        result = real_reader.read("SELECT COUNT(*) AS cnt FROM dbt_mrt.dim_patients")
        assert result[0]["cnt"] > 0, "dim_patients is empty"

    def test_dim_patients_no_duplicate_patient_ids(self, real_reader):
        result = real_reader.read("""
            SELECT COUNT(*) AS cnt
            FROM (
                SELECT patient_id
                FROM dbt_mrt.dim_patients
                GROUP BY patient_id
                HAVING COUNT(*) > 1
            ) dupes
        """)
        assert result[0]["cnt"] == 0, "dim_patients has duplicate patient_ids"

    def test_fct_ed_visits_all_patients_exist_in_dim(self, real_reader):
        result = real_reader.read("""
            SELECT COUNT(*) AS cnt
            FROM dbt_mrt.fct_ed_visits f
            LEFT JOIN dbt_mrt.dim_patients p ON f.patient_id = p.patient_id
            WHERE p.patient_id IS NULL
        """)
        assert result[0]["cnt"] == 0, "fct_ed_visits has patient_ids not in dim_patients"

    def test_fct_ed_visits_acuity_in_valid_range(self, real_reader):
        result = real_reader.read("""
            SELECT COUNT(*) AS cnt
            FROM dbt_mrt.fct_ed_visits
            WHERE acuity_level NOT IN (1,2,3,4,5)
            AND acuity_level IS NOT NULL
        """)
        assert result[0]["cnt"] == 0, "fct_ed_visits has invalid acuity values"

    def test_dim_date_covers_all_arrival_dates(self, real_reader):
        result = real_reader.read("""
            SELECT COUNT(*) AS cnt
            FROM dbt_mrt.fct_ed_visits f
            LEFT JOIN dbt_mrt.dim_date d ON f.arrival_date = d.full_date
            WHERE d.full_date IS NULL
        """)
        assert result[0]["cnt"] == 0, "Some arrival_dates not covered by dim_date"

    def test_bridge_triage_complaints_valid_stay_ids(self,real_reader):
        result = real_reader.read("""
            SELECT COUNT(*) AS cnt
            FROM dbt_mrt.bridge_triage_complaints b
            LEFT JOIN dbt_mrt.fct_ed_visits f ON b.stay_id = f.stay_id
            WHERE f.stay_id IS NULL
        """)
        assert result[0]["cnt"] == 0, "bridge_triage_complaints has invalid stay_ids"