"""Base de connaissances AMB TRANSPORTS 69 — chargee dans la memoire de chaque agent."""

COMPANY_PROFILE = """
# BASE DE CONNAISSANCES — AMB TRANSPORTS 69

## IDENTITE JURIDIQUE
- Denomination : AMB TRANSPORTS 69
- Forme juridique : SASU (Societe par Actions Simplifiee a associe unique)
- SIREN : 894 282 771
- SIRET : 894 282 771 00019
- RCS : 894 282 771 R.C.S. Lyon
- Code NAF/APE : 4941B — Transports routiers de fret de proximite
- Capital social : 10 000 EUR
- Immatriculation : 18/02/2021
- Debut d'activite : 06/02/2024
- Duree : 99 ans (jusqu'au 18/02/2120)
- Cloture exercice : 31 decembre
- Greffe : Tribunal des Activites Economiques de Lyon

## SIEGE SOCIAL
- Adresse : 23 B Route d'Heyrieux, 69800 Saint-Priest
- Email : contact@amb-transports.com
- Departement : Rhone (69), Region Auvergne-Rhone-Alpes

## DIRIGEANT — PRESIDENT & ASSOCIE UNIQUE
- Nom : Dennis BOATENG
- Ne le : 08/09/1990 a Bron (69500)
- Nationalite : Francaise
- Mandat : Duree indeterminee
- Pouvoirs : Pleins pouvoirs pour agir au nom de la Societe

## OBJET SOCIAL
1. Transport public routier de marchandises et location de vehicules avec conducteur
2. Courtage achat-revente de vehicules (neuf et occasion)
3. Achat-revente de vehicules neufs et d'occasion
4. Location de vehicules sans chauffeur
5. Apporteur d'affaires (hors immobilier)
6. Achat-revente de palettes
7. Achat-vente de pieces automobile
8. Import-export
9. Participation a des entreprises ou societes
10. Operations commerciales et financieres connexes

## LICENCES & CERTIFICATIONS
- Attestation capacite transport routier leger : N° JMP 84 25 00745 (delivree le 12/08/2025)
- Licence transport international : N° 2026/84/0000154 (valide du 22/02/2026 au 21/02/2036)
- Autorisation DREAL : delivree le 05/04/2024

## DONNEES FINANCIERES

### Exercice 2024
- Chiffre d'affaires : 153 008 EUR
- Total bilan : 62 453 EUR
- Resultat net : 7 378 EUR (benefice)
- Resultat d'exploitation : 8 967 EUR
- Capitaux propres : 28 438 EUR
- Total dettes : 34 015 EUR
- Salaires : 18 553 EUR
- Charges sociales : 7 267 EUR
- Charges externes : 125 601 EUR (82% du CA)

### Exercice 2023
- Chiffre d'affaires : 146 999 EUR
- Total bilan : 37 790 EUR
- Resultat net : 7 278 EUR

### Evolution 2023 → 2024
- CA : +4% (+6 009 EUR)
- Bilan : +65%
- Resultat net : stable (+1%)
- Salaires : -35% (reduction effectif)
- Charges externes : +24%

## PARC DE VEHICULES (7 vehicules)
1. Audi A3 (FZ-020-ZC) — Vehicule de service
2. Iveco 20m3 (GP-887-HN) — Porteur transport lourd
3. Mercedes Sprinter (FJ-936-HH) — Utilitaire
4. Mercedes Sprinter (FR-313-WF) — Utilitaire
5. Renault Trafic (GG-152-SE) — Utilitaire
6. Renault Trafic (GR-515-PY) — Utilitaire
7. Velo cargo — Livraison urbaine

## EQUIPE (mars 2026)
- Dennis BOATENG — President
- AHIMAH Emmanuel — Chauffeur (CDI)
- BOUKAIBA Youssef — Chauffeur
- JAABOUKI Zakariya — Chauffeur

## CLIENTS PRINCIPAUX
- TCS (Tournees SAV pieces materielles)
- Teleperformance
- Universite (contrat institutionnel)
- X Press Line

## COMPTABILITE
- Cabinet : Gestion Consulting, 15 rue des freres Lumiere, 69680 Chassieu
- Expert-comptable : Gilles BUND
- Email : gestionconsulting69@gmail.com
- Logiciel : ISACOMPTA CONNECT
- Regime fiscal : IS — Reel simplifie
- TVA : Regime normal

## ASSURANCES
- Assurance entreprise de transport souscrite
- Convention de gestion sinistres (Cat Gestion)

## ECHEANCES IMPORTANTES
- Licence transport international : valide jusqu'au 21/02/2036
- Cloture exercice 2025 : 31 decembre 2025
- DUERP : mise a jour annuelle requise
- DREAL : a surveiller

## DOCUMENTS EN PLACE
- DUERP (version 2026)
- Reglement interieur
- Registre RGPD
- Affichages obligatoires
- Convention SIDECAR (remboursement gazole 2026)
- Registre beneficiaires effectifs
- Attestation regularite fiscale
- Attestation URSSAF

## MARKETING
- Logo professionnel (AI, TIF, JPG, PNG)
- Flyer numerique et impression
- Cover LinkedIn
- Signature email
- Charte graphique definie
"""


def get_company_context() -> str:
    """Retourne le profil complet de l'entreprise."""
    return COMPANY_PROFILE


def get_agent_company_prompt(agent_role: str) -> str:
    """Retourne un prompt adapte au role de l'agent avec les infos de l'entreprise."""
    return (
        f"Tu travailles pour l'entreprise AMB TRANSPORTS 69. "
        f"Voici toutes les informations sur l'entreprise que tu dois connaitre et utiliser "
        f"dans tes reponses :\n\n{COMPANY_PROFILE}\n\n"
        f"Utilise ces informations pour personnaliser tes reponses. "
        f"Par exemple, utilise le vrai nom de l'entreprise, l'adresse, le SIRET, "
        f"les chiffres financiers, les vehicules, les employes, etc. "
        f"Le dirigeant s'appelle Dennis BOATENG."
    )
