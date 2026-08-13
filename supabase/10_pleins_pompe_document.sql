-- =====================================================================
-- AMB TRANSPORTS 69 — Suivi des dépenses de roulage
-- Fichier 10 : nature du document et numéro de pompe
-- À exécuter dans Supabase > SQL Editor, après les fichiers 1 à 9.
-- Ce fichier peut être relancé sans risque.
--
-- Deux renseignements qui manquaient pour départager les tickets :
--
--   · la POMPE. Le paiement à la pompe est plafonné : un chauffeur fait
--     parfois trois pleins du même montant dans la journée. Le numéro de
--     pompe, avec l'heure, distingue un vrai second plein d'un ticket
--     photographié deux fois.
--
--   · la NATURE du document. Le terminal imprime aussi des duplicata et
--     des reçus de pré-autorisation — le montant bloqué avant de servir.
--     Ce ne sont pas des justificatifs de dépense : les compter reviendrait
--     à payer deux fois le même plein.
-- =====================================================================

do $$ begin
  create type nature_document as enum (
    'ticket',            -- le vrai justificatif
    'duplicata',         -- réimpression d'un ticket déjà émis
    'pre_autorisation',  -- montant bloqué avant de servir, pas une dépense
    'indetermine'
  );
exception when duplicate_object then null; end $$;

alter table public.pleins
  add column if not exists pompe    text,
  add column if not exists document nature_document not null default 'ticket';

comment on column public.pleins.pompe is
  'Numéro de pompe ou de piste, tel qu''imprimé. Sert à distinguer deux pleins du même montant le même jour.';
comment on column public.pleins.document is
  'Nature du papier photographié. Un duplicata ou une pré-autorisation n''est pas un justificatif de dépense.';

create index if not exists idx_pleins_document on public.pleins(document)
  where document <> 'ticket';

-- ---------------------------------------------------------------------
-- Vérification
-- ---------------------------------------------------------------------
select document, count(*) as nb
  from public.pleins
 group by document
 order by nb desc;
