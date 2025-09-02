-- Seed data for healthcare providers in Cameroon
-- This script populates the providers table with realistic data around Douala and Yaoundé

USE healthlinkai;

-- Insert healthcare providers around Douala and Yaoundé
INSERT INTO providers (name, type, phone, email, address, city, lat, lng) VALUES 
-- Douala Providers
(
    'Hôpital Général de Douala',
    'hospital',
    '+237 233 42 24 69',
    'contact@hgd.cm',
    'Boulevard de la Liberté, Akwa',
    'Douala',
    4.0511,
    9.7679
),
(
    'Clinique des Spécialités de Douala',
    'clinic',
    '+237 233 43 15 82',
    'info@clinique-specialites.cm',
    'Rue Joss, Bonanjo',
    'Douala',
    4.0469,
    9.7009
),
(
    'Pharmacie du Rond-Point Deido',
    'pharmacy',
    '+237 233 40 28 91',
    'pharmacie.deido@gmail.com',
    'Rond-Point Deido, Avenue Charles de Gaulle',
    'Douala',
    4.0614,
    9.7086
),
(
    'Centre de Counseling MindWell Douala',
    'counseling',
    '+237 690 45 78 92',
    'douala@mindwell.cm',
    'Quartier Bonapriso, Rue des Cocotiers',
    'Douala',
    4.0389,
    9.6947
),
(
    'Polyclinique Bonanjo',
    'clinic',
    '+237 233 42 67 34',
    'accueil@polyclinique-bonanjo.cm',
    'Avenue Ahidjo, Bonanjo',
    'Douala',
    4.0501,
    9.6998
),
(
    'Pharmacie Centrale Akwa',
    'pharmacy',
    '+237 233 42 18 55',
    'pharmacie.akwa@yahoo.fr',
    'Rue Gallieni, Akwa',
    'Douala',
    4.0489,
    9.7612

),

-- Yaoundé Providers
(
    'Hôpital Central de Yaoundé',
    'hospital',
    '+237 222 23 40 06',
    'direction@hcy.cm',
    'Avenue Henri Dunant, Centre-ville',
    'Yaoundé',
    3.8480,
    11.5021
),
(
    'Clinique Universitaire',
    'clinic',
    '+237 222 20 15 33',
    'contact@clinique-universitaire.cm',
    'Quartier Ngoa-Ekellé',
    'Yaoundé',
    3.8667,
    11.5167
),
(
    'Centre Psychiatrique de Jamot',
    'counseling',
    '+237 222 23 14 67',
    'jamot.psy@gmail.com',
    'Hôpital Jamot, Quartier Ekounou',
    'Yaoundé',
    3.8378,
    11.5230
),
(
    'Pharmacie de la Poste Centrale',
    'pharmacy',
    '+237 222 23 56 78',
    'pharmacie.poste@hotmail.com',
    'Avenue Kennedy, Centre-ville',
    'Yaoundé',
    3.8634,
    11.5158
),
(
    'Polyclinique les Palmiers',
    'clinic',
    '+237 222 20 89 45',
    'info@palmiers-clinic.cm',
    'Quartier Bastos, Rue 1.750',
    'Yaoundé',
    3.8856,
    11.5342
),
(
    'Centre de Santé Mentale Essos',
    'counseling',
    '+237 690 12 34 56',
    'essos.mental@mindhealth.cm',
    'Quartier Essos, près du Lycée Général Leclerc',
    'Yaoundé',
    3.8445,
    11.4889
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_providers_type ON providers(type);
CREATE INDEX IF NOT EXISTS idx_providers_city ON providers(city);
CREATE INDEX IF NOT EXISTS idx_providers_location ON providers(lat, lng);

-- Verify the data was inserted
SELECT 
    COUNT(*) as total_providers,
    city,
    type,
    COUNT(*) as count_by_type
FROM providers 
GROUP BY city, type
ORDER BY city, type;
