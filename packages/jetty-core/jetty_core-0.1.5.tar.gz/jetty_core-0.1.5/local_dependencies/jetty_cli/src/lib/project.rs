//! Path utilities for project organization.
//!
//! The project structure currently looks like this:
//!
//! ```text
//! pwd
//!  └── {project_name}
//!       ├── jetty_config.yaml
//!       ├── .data
//!       │    ├── jetty_graph
//!       │    └── {connector}
//!       │         └── {connector-specific data}
//!       └── tags
//!            └── tags.yaml
//! ```

use std::path::{Path, PathBuf};

use dirs::home_dir;
use lazy_static::lazy_static;

lazy_static! {
    static ref TAGS_DIR: PathBuf = PathBuf::from("tags");
    static ref DATA_DIR: PathBuf = PathBuf::from(".data");
    static ref TAGS_CFG: PathBuf = PathBuf::from("tags.yaml");
    static ref JETTY_CFG: PathBuf = PathBuf::from("jetty_config.yaml");
    static ref CONNECTOR_CFG: PathBuf = PathBuf::from("connectors.yaml");
    static ref PROFILE_CFG_DIR: PathBuf = PathBuf::from(".jetty");
    static ref JETTY_GRAPH: PathBuf = PathBuf::from("jetty_graph");
    static ref DEFAULT_KEY_DIR: PathBuf = PathBuf::from(".ssh");
}

pub(crate) fn tags_cfg_path<P: AsRef<Path>>(project_path: P) -> PathBuf {
    project_path.as_ref().join(tags_cfg_path_local())
}

/// Local path for the tags config.
pub(crate) fn tags_cfg_path_local() -> PathBuf {
    TAGS_DIR.as_path().join(TAGS_CFG.as_path())
}

/// Path for the connector config.
pub(crate) fn connector_cfg_path() -> PathBuf {
    home_dir()
        .expect("getting home dir")
        .join(PROFILE_CFG_DIR.as_path())
        .join(CONNECTOR_CFG.as_path())
}

pub(crate) fn jetty_cfg_path<P: AsRef<Path>>(project_path: P) -> PathBuf {
    project_path.as_ref().join(JETTY_CFG.as_path())
}

/// Local path for the jetty config.
pub(crate) fn jetty_cfg_path_local() -> PathBuf {
    JETTY_CFG.clone()
}

pub(crate) fn data_dir() -> PathBuf {
    DATA_DIR.clone()
}

pub(crate) fn graph_filename() -> PathBuf {
    JETTY_GRAPH.clone()
}

pub(crate) fn default_keypair_dir_path() -> PathBuf {
    home_dir()
        .expect("getting home dir")
        .join(DEFAULT_KEY_DIR.as_path())
}

pub(crate) fn user_id_file() -> PathBuf {
    home_dir()
        .expect("getting home dir")
        .join(PROFILE_CFG_DIR.as_path())
        .join("uid")
}
