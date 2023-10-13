export default function (req, res) {
  const report = req.body;

  // You can log, store, or process the CSP report as needed.
  // For this example, we'll just log it.
  console.log("CSP Report:", report);

  // Respond with a 204 No Content status.
  res.status(204).end();
}
