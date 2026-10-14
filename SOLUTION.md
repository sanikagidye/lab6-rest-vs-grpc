# Lab 6 - REST vs gRPC Performance

All values are in milliseconds per operation.

| Method | Local | Same-Zone | Different Region |
|---|---:|---:|---:|
| REST add | 5.000 | 5.128 | 377.231 |
| gRPC add | 0.970 | 1.784 | 165.164 |
| REST rawimg | 9.659 | 12.700 | 1491.135 |
| gRPC rawimg | 20.258 | 16.899 | 187.450 |
| REST dotproduct | 5.628 | 5.620 | 372.035 |
| gRPC dotproduct | 1.116 | 1.985 | 155.303 |
| REST jsonimg | 48.888 | 53.087 | 1648.081 |
| gRPC jsonimg | 46.488 | 43.976 | 216.249 |
| PING | 0.049 | 0.607 | 178.360 |

The results show that network latency has a major impact on RPC performance. Local and same-zone calls were fast, while the different-region calls were much slower, which matches the increase in ping latency from 0.049 ms locally and 0.607 ms in the same zone to 178.360 ms across regions. gRPC was generally faster than REST, especially for the `add` and `dotproduct` methods and for cross-region image transfers. One important reason is that REST creates a new TCP connection for each query, while gRPC reuses a single TCP connection for multiple queries, reducing connection setup overhead. This difference becomes much more important when network latency is high. The image operations also showed a large performance gap across regions, with gRPC significantly outperforming REST, especially for `rawimg` and `jsonimg`.
