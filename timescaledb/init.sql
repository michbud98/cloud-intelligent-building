CREATE TABLE IF NOT EXISTS sensor_measurements (
   time        TIMESTAMPTZ NOT NULL,
   sensor_id   TEXT NOT NULL,
   room        TEXT,
   board_type  TEXT,
   sensor_type TEXT,
   temperature DOUBLE PRECISION,
   pressure    DOUBLE PRECISION,
   humidity    DOUBLE PRECISION,
   gas_resistance    DOUBLE PRECISION,
   iaq    DOUBLE PRECISION
);

SELECT create_hypertable('sensor_measurements', by_range('time', INTERVAL '1 month'), if_not_exists => TRUE);

-- Add a retention policy to the hypertable --
-- SELECT add_retention_policy('sensor_measurements', INTERVAL '3 months');

CREATE TABLE IF NOT EXISTS boiler_measurements (
   time        TIMESTAMPTZ NOT NULL,
   sensor_id   TEXT NOT NULL,
   board_type  TEXT,
   sensor_type TEXT,
   tmp_in DOUBLE PRECISION,
   tmp_out DOUBLE PRECISION,
   dhw_tmp DOUBLE PRECISION,
   dhw_coil_tmp DOUBLE PRECISION
);

SELECT create_hypertable('boiler_measurements', by_range('time', INTERVAL '1 month'), if_not_exists => TRUE);

-- Add a retention policy to the hypertable --
-- SELECT add_retention_policy('boiler_measurements', INTERVAL '3 months');

CREATE TABLE IF NOT EXISTS sensors (
    sensor_id TEXT UNIQUE NOT NULL,
    room TEXT
);