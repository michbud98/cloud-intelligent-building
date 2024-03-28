CREATE TABLE IF NOT EXISTS sensor_measurements (
   time        TIMESTAMPTZ NOT NULL,
   sensor_id   TEXT NOT NULL,
   room        TEXT,
   board_type  TEXT,
   sensor_type TEXT,
   temperature DOUBLE PRECISION,
   pressure    DOUBLE PRECISION,
   humidity    DOUBLE PRECISION
);

SELECT create_hypertable('sensor_measurements', by_range('time'), if_not_exists => TRUE);

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

SELECT create_hypertable('boiler_measurements', by_range('time'), if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS sensors (
    sensor_id TEXT UNIQUE NOT NULL,
    room TEXT
);