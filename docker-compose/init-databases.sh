#!/bin/bash

# create instances database
psql -U postgres -c 'CREATE DATABASE instances'
psql -U postgres -d instances -c 'CREATE TABLE IF NOT EXISTS entities (entity_uuid integer, inf_id integer, att_tech text[], name text, external_id text, type text, whitelist_uuid integer, child integer[], parent integer, state text, metadata json, PRIMARY KEY(entity_uuid))'

# create verifiers database
psql -U postgres -c 'CREATE DATABASE attestation_tech'
psql -U postgres -d attestation_tech -c 'CREATE TABLE IF NOT EXISTS verifiers (att_tech text, inf_id integer, metadata json, PRIMARY KEY(att_tech, inf_id))'

# create policy database
psql -U postgres -c 'CREATE DATABASE policy'
psql -U postgres -d policy -c 'CREATE TABLE IF NOT EXISTS policies (entity_uuid integer, policy text, PRIMARY KEY(entity_uuid))'