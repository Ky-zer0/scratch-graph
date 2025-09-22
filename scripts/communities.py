
import igraph as ig
import pandas as pd
import leidenalg as la

users = pd.read_csv("mapping.csv")

g = ig.Graph.Read_GraphML("scratch_network.graphml")
print(f"Graph has {g.vcount()} nodes and {g.ecount()} edges.")

communities = la.find_partition(
    g, 
    la.ModularityVertexPartition, 
    seed=42  # for reproducibility
)

memberships=communities.membership
sizes = communities.sizes()
print(communities.modularity)

# Pair (community_index, size)
indexed_sizes = list(enumerate(sizes))
# Sort by size descending
indexed_sizes.sort(key=lambda x: x[1], reverse=True)

print("Largest 10 communities:")
for comm, size in indexed_sizes[:10]:
    print(f"Community {comm}: {size} nodes")

comm_df = pd.DataFrame({
    "id": g.vs["id"],
    "community": memberships
})
comm_df['id']=comm_df['id'].str.lstrip("n").astype(int)
print(comm_df.head())

merged = users.merge(comm_df, on="id", how="inner")

#merged.to_csv("users_with_communities_res_3.csv", index=False)