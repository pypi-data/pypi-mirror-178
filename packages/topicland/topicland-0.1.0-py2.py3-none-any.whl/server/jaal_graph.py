
from sqlalchemy import create_engine
import pandas as pd
from jaal import Jaal

def main() -> None:

    pd.set_option('display.expand_frame_repr', False)

    sql_engine = create_engine('mysql+pymysql://root:root@127.0.0.1', pool_recycle=3600)
    with sql_engine.connect() as connection:
        nodes_df = pd.read_sql("select * from cyberpunk_edgerunner.nodes", connection);
        new_nodes_df = nodes_df.rename(columns={"id": "uid", "name": "id"})
        #print(new_nodes_df)

        edges_df = pd.read_sql("select * from cyberpunk_edgerunner.edges", connection);
        new_edges_df = edges_df.rename(columns={"source": "from", "target": "to"})
        #print(new_edges_df)

        Jaal(new_edges_df, new_nodes_df).plot()

if __name__ == "__main__":
    main()
