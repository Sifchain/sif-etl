-- public.pmtp_pool_info definition

-- Drop table

-- DROP TABLE public.pmtp_pool_info;

CREATE TABLE public.pmtp_pool_info (
	height int4 NULL,
	pool varchar NULL,
	native_asset_balance numeric NULL,
	external_asset_balance numeric NULL,
	asset_balance_in_usd numeric NULL,
	native_asset_bal_usd numeric NULL,
	external_asset_bal_usd numeric NULL,
	external_price_usd numeric NULL,
	native_price_usd numeric NULL,
	pool_units numeric NULL
);

-- public.pmtp_pool definition

-- Drop table

-- DROP TABLE public.pmtp_pool;

CREATE TABLE public.pmtp_pool (
	height int4 NULL,
	pool varchar NULL,
	native_asset_balance numeric NULL,
	external_asset_balance numeric NULL,
	asset_balance_in_usd numeric NULL,
	native_asset_bal_usd numeric NULL,
	external_asset_bal_usd numeric NULL,
	external_price_usd numeric NULL,
	native_price_usd numeric NULL,
	"timestamp" timestamptz NOT NULL DEFAULT now(),
	pool_units numeric NULL
);
CREATE INDEX pmtp_pool_height_idx ON public.pmtp_pool USING btree (height);
CREATE INDEX pmtp_pool_pool_idx ON public.pmtp_pool USING btree (pool);
CREATE INDEX pmtp_pool_timestamp_idx ON public.pmtp_pool USING btree ("timestamp" DESC);

-- Table Triggers

create trigger ts_insert_blocker before
insert
    on
    public.pmtp_pool for each row execute function _timescaledb_internal.insert_blocker();

CREATE TABLE public.pool_info (
	height int4 NULL,
	pool varchar NULL,
	native_asset_balance numeric NULL,
	external_asset_balance numeric NULL,
	asset_balance_in_usd numeric NULL,
	native_asset_bal_usd numeric NULL,
	external_asset_bal_usd numeric NULL,
	external_price_usd numeric NULL,
	native_price_usd numeric NULL
);
CREATE INDEX pool_info_pool_idx ON public.pool_info USING btree (pool);

-- public.tokenprices_coinmarketcap definition

-- Drop table

-- DROP TABLE public.tokenprices_coinmarketcap;

CREATE TABLE public.tokenprices_coinmarketcap (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"timestamp" timestamptz(0) NOT NULL,
	"token" varchar NOT NULL,
	circulating_supply numeric NULL,
	total_supply numeric NULL,
	last_updated timestamptz(0) NULL,
	last_price numeric NULL,
	volume_24h numeric NULL,
	market_cap numeric NULL,
	percent_change_1h float4 NULL,
	percent_change_24h float4 NULL,
	percent_change_7d float4 NULL,
	percent_change_30d float4 NULL,
	percent_change_60d float4 NULL,
	percent_change_90d float4 NULL,
	cmc_rank int4 NULL,
	is_latest bool NOT NULL DEFAULT true,
	CONSTRAINT tokenprices_coinmarketcap_un UNIQUE ("timestamp", token)
);
CREATE INDEX tokenprices_coinmarketcap_is_latest_idx ON public.tokenprices_coinmarketcap USING btree (is_latest);
CREATE INDEX tokenprices_coinmarketcap_timestamp_idx ON public.tokenprices_coinmarketcap USING btree ("timestamp" DESC);
CREATE INDEX tokenprices_coinmarketcap_token_timestamp_idx ON public.tokenprices_coinmarketcap USING btree (token, "timestamp" DESC);

-- Table Triggers

create trigger ts_insert_blocker before
insert
    on
    public.tokenprices_coinmarketcap for each row execute function _timescaledb_internal.insert_blocker();


-- public.tokenprices_staging definition

-- Drop table

-- DROP TABLE public.tokenprices_staging;

CREATE TABLE public.tokenprices_staging (
	"time" timestamptz NULL,
	asset_price float8 NULL,
	asset varchar(15) NULL,
	height int8 NULL,
	is_interpolated bool NULL,
	reward_distributed float8 NULL
);

CREATE TABLE POOLS (
	created_at TIMESTAMP DEFAULT NOW(),
	pool_data json,
	id serial NOT NULL PRIMARY KEY
);

CREATE TABLE PRICES (
	height INT UNIQUE,
	timestamp TIMESTAMPTZ,
	rowan_cusdt NUMERIC,
	token_prices json,
	token_volumes_24hr json,
	id serial NOT NULL PRIMARY KEY
);
-- public.token_registry definition

-- Drop table

DROP TABLE if exists token_registry;

CREATE TABLE token_registry (
	base_denom varchar NOT NULL,
	denom varchar NOT NULL,
	decimals int4 NOT NULL,
	modified timestamptz NOT NULL,
	is_active bool NOT NULL
);
CREATE INDEX token_registry_base_denom_idx ON public.token_registry USING btree (base_denom);
CREATE INDEX token_registry_denom_idx ON public.token_registry USING btree (denom);

DROP TABLE IF EXISTS TokenPrices;


CREATE TABLE public.tokenprices (
	"time" timestamptz NOT NULL,
	asset_price float8 NULL,
	asset varchar(15) NULL,
	height int8 NULL,
	is_interpolated bool NOT NULL DEFAULT false,
	reward_distributed float8 NULL,
	CONSTRAINT tokenprices_un UNIQUE ("time", asset, height)
);
CREATE INDEX tokenprices_asset_idx ON public.tokenprices USING btree (asset);
CREATE INDEX tokenprices_asset_time_idx ON public.tokenprices USING btree (asset, "time" DESC);
CREATE INDEX tokenprices_height_idx ON public.tokenprices USING btree (height);
CREATE INDEX tokenprices_time_idx ON public.tokenprices USING btree ("time" DESC);

SELECT create_hypertable('TokenPrices', 'time', 'asset', 2);


-- Add TokenVolume to track daily traded volumes
DROP TABLE IF EXISTS TokenVolumes;

CREATE TABLE TokenVolumes (
	"time" timestamptz NOT NULL,
	asset_volume_daily float8 NULL,
	asset varchar(15) NULL,
	height int8 NULL
);

SELECT create_hypertable('TokenVolumes', 'time', 'asset', 2);

CREATE index on TokenVolumes(height);

-- Decompose JSON for Token Rates from Prices table to TokenPrices table
CREATE OR REPLACE PROCEDURE ADD_TOKENPRICES()
language SQL
as $$
	insert into TokenPrices
	(height, asset_price, asset, time)
	select  f.height, cast(p.token_prices ->> f.tok as float) asset_price, f.tok as asset, p."timestamp" 
	from (
		select height, json_object_keys(token_prices) as tok from prices ) f inner join
		prices p on f.height = p.height
		and p.height not in (select distinct height from TokenPrices);

    insert into TokenVolumes
	  (height, asset_volume_daily, asset, time)
	  select p.height, cast(p.token_volumes_24hr ->> f.tok as numeric) as asset_volume_daily , f.tok as asset, p.timestamp  
	  from (
		  select height, json_object_keys(token_volumes_24hr) as tok from prices ) f inner join
		  prices p on f.height = p.height
		  and p.height not in (select distinct height from TokenVolumes);
$$;

-- public.events_audit definition

-- Drop table

-- DROP TABLE public.events_audit;

CREATE TABLE public.events_audit (
	height int8 NULL,
	"type" varchar NOT NULL,
	"time" timestamptz(0) NOT NULL,
	hash varchar NULL,
	log jsonb NOT NULL,
	al_token varchar NULL,
	al_provider varchar NULL,
	al_amount numeric NULL,
	al_token2 varchar NULL,
	al_amount2 numeric NULL,
	rl_provider varchar NULL,
	rl_token varchar NULL,
	rl_amount numeric NULL,
	swap_begin_recipient varchar NULL,
	swap_begin_sender varchar NULL,
	swap_begin_amount numeric NULL,
	swap_begin_token varchar NULL,
	swap_final_recipient varchar NULL,
	swap_final_sender varchar NULL,
	swap_final_amount numeric NULL,
	swap_final_token varchar NULL,
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	rl_token2 varchar NULL,
	rl_amount2 numeric NULL,
	swap_liquidity_fee numeric NULL,
	swap_price_impact numeric NULL,
	de_validator_addr varchar NULL,
	de_amount numeric NULL,
	de_sender_addr varchar NULL,
	de_gas_wanted numeric NULL,
	de_gas_used varchar NULL,
	wr_recipient_addr varchar NULL,
	wr_sender_addr varchar NULL,
	wr_amount numeric NULL,
	wr_token varchar NULL,
	lk_sender varchar NULL,
	lk_recipient varchar NULL,
	lk_amount numeric NULL,
	lk_token varchar NULL,
	lk_amount2 numeric NULL,
	lk_token2 varchar NULL,
	re_recipient_addr varchar NULL,
	re_sender_addr varchar NULL,
	re_amount numeric NULL,
	re_token varchar NULL,
	re_gas_wanted numeric NULL,
	re_gas_used numeric NULL,
	bn_recipient varchar NULL,
	bn_sender varchar NULL,
	bn_amount numeric NULL,
	bn_token varchar NULL,
	bn_amount2 varchar NULL,
	bn_token2 varchar NULL,
	cc_recipient_addr varchar NULL,
	cc_sender_addr varchar NULL,
	cc_amount numeric NULL,
	cc_token varchar NULL,
	cc_claim_type varchar NULL,
	cc_module varchar NULL,
	cc_prophecy_status varchar NULL,
	ub_begin_recipient varchar NULL,
	ub_begin_sender varchar NULL,
	ub_begin_amount numeric NULL,
	ub_begin_token varchar NULL,
	ub_final_recipient varchar NULL,
	ub_final_sender varchar NULL,
	ub_final_amount numeric NULL,
	ub_final_token varchar NULL,
	al_pool varchar NULL,
	rl_pool varchar NULL,
	cv_validator_addr varchar NULL,
	cv_sender_addr varchar NULL,
	cv_amount numeric NULL,
	cv_token varchar NULL,
	cv_gas_wanted numeric NULL,
	cv_gas_used numeric NULL,
	ev_sender varchar NULL,
	ev_min_self_delegation numeric NULL,
	ev_commission_rate numeric NULL,
	ev_max_commission_change_rate numeric NULL,
	ev_max_commission_rate numeric NULL,
	ev_gas_wanted numeric NULL,
	ev_gas_used numeric NULL,
	pv_sender varchar NULL,
	pv_vote varchar NULL,
	pv_gaswanted numeric NULL,
	pv_gasused numeric NULL,
	pd_sender varchar NULL,
	pd_recipient varchar NULL,
	pd_proposal_type varchar NULL,
	pd_voting_period_start numeric NULL,
	pd_token varchar NULL,
	pd_amount numeric NULL,
	pd_gaswanted numeric NULL,
	pd_gasused numeric NULL,
	ds_sender varchar NULL,
	ds_recipient varchar NULL,
	ds_action varchar NULL,
	ds_token varchar NULL,
	ds_amount numeric NULL,
	ds_gaswanted numeric NULL,
	ds_gasused numeric NULL,
	dt_receiver varchar NULL,
	dt_sender varchar NULL,
	dt_denom varchar NULL,
	dt_amount numeric NULL,
	dt_success bool NULL,
	dt_packet_src_port varchar NULL,
	dt_packet_src_channel varchar NULL,
	dt_packet_dst_port varchar NULL,
	dt_packet_dst_channel varchar NULL,
	dt_packet_channel_ordering varchar NULL,
	dt_packet_connection varchar NULL,
	dt_packet_timeout_timestamp numeric NULL,
	dt_packet_timeout_height varchar NULL,
	dt_packet_sequence varchar NULL,
	description varchar NULL,
	uc_client_id varchar NULL,
	uc_client_type varchar NULL,
	uc_consensus_height varchar NULL,
	uc_header varchar NULL,
	uc_module varchar NULL,
	ap_success varchar NULL,
	ap_module varchar NULL,
	ul_address varchar NULL,
	ul_unit numeric NULL,
	ul_pool varchar NULL,
	ld_recipient_addr varchar NULL,
	ld_total_amount numeric NULL,
	ld_amount jsonb NULL,
	CONSTRAINT events_audit_pk PRIMARY KEY (id, "time", type),
	CONSTRAINT events_audit_un UNIQUE (type, "time", hash)
);
CREATE INDEX events_audit_al_provider_idx ON public.events_audit USING btree (al_provider, al_pool);
CREATE INDEX events_audit_height_idx ON public.events_audit USING btree (height);
CREATE INDEX events_audit_rl_provider_idx ON public.events_audit USING btree (rl_provider, rl_pool);
CREATE INDEX events_audit_swap_begin_token_idx ON public.events_audit USING btree (swap_begin_token, swap_final_token);
CREATE INDEX events_audit_swap_final_token_idx ON public.events_audit USING btree (swap_final_token, swap_begin_token);
CREATE INDEX events_audit_time_idx ON public.events_audit USING btree ("time" DESC);
CREATE INDEX events_audit_type_time_idx ON public.events_audit USING btree (type, "time" DESC);

-- Table Triggers

create trigger ts_insert_blocker before
insert
    on
    public.events_audit for each row execute function _timescaledb_internal.insert_blocker();

-- Table Triggers
-- public.events_audit_txn definition

-- Drop table

-- DROP TABLE public.events_audit_txn;

CREATE TABLE public.events_audit_txn (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	event_audit_id int8 NOT NULL,
	height int8 NOT NULL,
	"time" timestamptz(0) NOT NULL,
	txn_type varchar NULL,
	amount numeric NULL,
	"validator" varchar NULL,
	hash varchar NULL,
	recipient varchar NULL,
	sender varchar NULL,
	"token" varchar NULL,
	CONSTRAINT events_audit_txn_pk PRIMARY KEY (id,height,"time",event_audit_id),
	CONSTRAINT events_audit_txn_un UNIQUE (hash,"time",height,event_audit_id)
);
CREATE INDEX event_audit_txn_height_idx ON public.events_audit_txn (height);
CREATE INDEX event_audit_txn_txn_type_idx ON public.events_audit_txn (txn_type);
CREATE INDEX events_audit_txn_height_time_idx ON public.events_audit_txn (height,"time" DESC);
CREATE INDEX events_audit_txn_time_idx ON public.events_audit_txn ("time" DESC);


-- public.tokenprices_staging definition

-- Drop table

DROP TABLE if exists tokenprices_staging;

CREATE TABLE tokenprices_staging (
	"time" timestamptz NULL,
	asset_price float8 NULL,
	asset varchar(15) NULL,
	height int8 NULL,
	is_interpolated bool NULL,
	reward_distributed float8 NULL
);
-- public.prices_latest definition

-- Drop table

DROP TABLE if exists public.prices_latest;

CREATE TABLE public.prices_latest (
	height int4 NOT NULL,
	"timestamp" timestamptz NOT NULL,
	rowan_cusdt numeric NULL,
	token_prices json NULL,
	token_volumes_24hr json NULL
);

-- public.trade_daily_temp definition

-- Drop table

DROP TABLE if exists public.trade_daily_temp;

CREATE TABLE public.trade_daily_temp (
	trading_pairs varchar(15) NULL,
	highest_price_24h float8 NULL,
	lowest_price_24h float8 NULL,
	last_price float8 NULL,
	opening float8 NULL,
	price_change_percent_24h float8 NULL,
	base_currency text NULL,
	target_currency text NULL,
	base_volume numeric NULL,
	target_volume numeric NULL,
	bid float8 NULL,
	ask float8 NULL,
	liquidity_in_usd numeric NULL
);
-- public.pmtp_pool_info definition

-- Drop table

DROP TABLE if exists public.pmtp_pool_info;

CREATE TABLE public.pmtp_pool_info (
	height int4 NULL,
	pool varchar NULL,
	native_asset_balance numeric NULL,
	external_asset_balance numeric NULL,
	asset_balance_in_usd numeric NULL,
	native_asset_bal_usd numeric NULL,
	external_asset_bal_usd numeric NULL,
	external_price_usd numeric NULL,
	native_price_usd numeric NULL,
	pool_units numeric NULL
);