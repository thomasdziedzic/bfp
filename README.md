Routes
======

Problem Routes
--------------

<table>
	<tr>
		<th>Route</th>
		<th>HTTP Method</th>
		<th>Example Request</th>
		<th>Example Response</th>
	</tr>
	<tr>
		<td>/problem</td>
		<td>POST</td>
		<td>{"description": "problem"}</td>
		<td>{"id": 1}</td>
	</tr>
	<tr>
		<td>/problems</td>
		<td>GET</td>
		<td></td>
		<td>[{"id": 1, "description": "problem"}]</td>
	</tr>
	<tr>
		<td>/problem/:id</td>
		<td>GET</td>
		<td></td>
		<td>{"ideas": [{"id": 1, "description": "idea"}],
			"description": "problem"}</td>
	</tr>
	<tr>
		<td>/problem/:id</td>
		<td>PUT</td>
		<td>{"description": "another problem"}</td>
		<td></td>
	</tr>
	<tr>
		<td>/problem/:id</td>
		<td>DELETE</td>
		<td></td>
		<td></td>
	</tr>
</table>

Idea Routes
--------------

<table>
	<tr>
		<th>Route</th>
		<th>HTTP Method</th>
		<th>Example Request</th>
		<th>Example Response</th>
	</tr>
	<tr>
		<td>/idea</td>
		<td>POST</td>
		<td>{"description": "idea"}</td>
		<td>{"id": 1}</td>
	</tr>
	<tr>
		<td>/ideas</td>
		<td>GET</td>
		<td></td>
		<td>[{"id": 1, "description": "idea"}]</td>
	</tr>
	<tr>
		<td>/idea/:id</td>
		<td>GET</td>
		<td></td>
		<td>{"problems": [{"id": 1, "description": "problem"}],
			"description": "idea"}</td>
	</tr>
	<tr>
		<td>/idea/:id</td>
		<td>PUT</td>
		<td>{"description": "another idea"}</td>
		<td></td>
	</tr>
	<tr>
		<td>/idea/:id</td>
		<td>DELETE</td>
		<td></td>
		<td></td>
	</tr>
</table>

ProblemIdea Routes
--------------

<table>
	<tr>
		<th>Route</th>
		<th>HTTP Method</th>
		<th>Example Request</th>
		<th>Example Response</th>
	</tr>
	<tr>
		<td>/problemidea/:problem_id/:idea_id</td>
		<td>POST</td>
		<td></td>
		<td></td>
	</tr>
	<tr>
		<td>/problemidea/:problem_id/:idea_id</td>
		<td>DELETE</td>
		<td></td>
		<td></td>
	</tr>
</table>

Search Routes
--------------

<table>
	<tr>
		<th>Route</th>
		<th>HTTP Method</th>
		<th>Example Request</th>
		<th>Example Response</th>
	</tr>
	<tr>
		<td>/search/problems</td>
		<td>POST</td>
		<td>{"query": "problem"}</td>
		<td>[{"id": 1, "description": "problem"}]</td>
	</tr>
	<tr>
		<td>/search/ideas</td>
		<td>POST</td>
		<td>{"query": "idea"}</td>
		<td>[{"id": 1, "description": "idea"}]</td>
	</tr>
</table>
