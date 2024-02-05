const nodes = [
                { id: 1, name: "John Doe", years: 53 },
                { id: 2, name: "Mike Doe", years: 25 },
                { id: 3, name: "Lucy Doe", years: 15 },
                { id: 4666, name: "ime", years: 12 }];


            const edges = [
                { source: 1, target: 2, data: { label: "Edge 1", key1: "value1", key2: "value2" } },
                { source: 2, target: 3, data: { label: "Edge 2", key1: "value3", key2: "value4" } },
                { source: 1, target: 4666, data: { label: "Edge 3", key1: "value5", key2: "value6" } },
                { source: 1, target: 3, data: { label: "Edge 4", key1: "value7", key2: "value8" } },
            ];

            const width = 1000;
            const height = 600;

            const svg = d3.select("#graph-container").append("svg")
                .attr("width", width)
                .attr("height", height)
                .call(d3.zoom().scaleExtent([0.1, 4]).on("zoom", zoomed))
                .append("g");

            const simulation = d3.forceSimulation(nodes)
                .force("charge", d3.forceManyBody().strength(-200))
                .force("link", d3.forceLink(edges).id(d => d.id).distance(150))
                .force("collide", d3.forceCollide(25))
                .force("center", d3.forceCenter(width / 2, height / 2));

            const linkElements = svg.selectAll(".link")
                .data(edges)
                .enter().append("line")
                .attr("class", "link")
                .attr("marker-end", "url(#arrow)")
                .on("mouseover", showDetails)
                .on("mouseout", hideDetails);

            const nodeElements = svg.selectAll(".node")
                .data(nodes)
                .enter().append("g")
                .attr("class", "node")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended))
                .on("mouseover", showDetails)
                .on("mouseout", hideDetails);

            nodeElements.append("circle")
                .attr("r", 20);

            nodeElements.append("text")
                .text(d => `ID: ${d.id}`)
                .attr("dy", 5);

            const edgeTextElements = svg.selectAll(".edge")
                .data(edges)
                .enter().append("text")
                .attr("class", "edge")
                .on("mouseover", showDetails)
                .on("mouseout", hideDetails);

            const arrowElements = svg.append("defs")
                .selectAll(".arrow")
                .data(edges)
                .enter().append("marker")
                .attr("class", "arrow")
                .attr("id", d => `arrow-${d.source.id}-${d.target.id}`)
                .attr("markerWidth", 10)
                .attr("markerHeight", 10)
                .attr("refX", 19)
                .attr("refY", 3)
                .attr("orient", "auto")
                .append("path")
                .attr("d", "M0,-5L10,0L0,5");

            linkElements.attr("marker-end", d => `url(#arrow-${d.source.id}-${d.target.id})`);

            simulation.on("tick", () => {
                linkElements
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                nodeElements
                    .attr("transform", d => `translate(${d.x},${d.y})`);

                edgeTextElements
                    .attr("x", d => (d.source.x + d.target.x) / 2)
                    .attr("y", d => (d.source.y + d.target.y) / 2);
            });

            d3.select("#graph-outline")
                .style("width", `${width}px`)
                .style("height", `${height}px`);

            function dragstarted(event, d) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }

            function dragended(event, d) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }

            function zoomed(event) {
                svg.attr("transform", event.transform);
            }

            function showDetails(event, d) {
                d3.select("#details")
                    .style("display", "block")
                    .html(JSON.stringify(d.data || d, null, 4));
            }

            function hideDetails() {
                d3.select("#details").style("display", "none");
            }