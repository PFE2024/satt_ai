const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello App!');
});

app.listen(port, () => {
  console.log(`satt app on 3000`);
});