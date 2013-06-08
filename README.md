Routes
======

<table>
	<tr>
		<th>Route</th>
		<th>HTTP Method</th>
		<th>Example Request</th>
		<th>Example Response</th>
	</tr>

	<tr>
		<td>/</td>
		<td>GET</td>
		<td></td>
		<td></td>
	</tr>

	<tr>
		<td>/problem</td>
		<td>POST</td>
		<td>{"description": "test"}</td>
		<td>{"id": 1}</td>
	</tr>
	<tr>
		<td>/problem/:id</td>
		<td>GET</td>
		<td></td>
		<td>{"ideas": [], "description": "test"}</td>
	</tr>
	<tr>
		<td>/problem/:id</td>
		<td>PATCH</td>
		<td>{"description": "another description"}</td>
		<td></td>
	</tr>
	<tr>
		<td>/problem/:id</td>
		<td>DELETE</td>
		<td></td>
		<td></td>
	</tr>
</table>

