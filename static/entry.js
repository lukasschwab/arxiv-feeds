console.log("RUNNING RUNNING RUNNING")

document.getElementById("query").addEventListener(
  'keypress',
  (event) => {
    console.log("GOT EVENT")
    if (event.keyCode === 13) {
      console.log("GOT ENTER")
      event.preventDefault();
      redirectToAtomFeed();
    }
  }
)
function redirectToAtomFeed() {
  console.log("TESTING")
  const query = document.getElementById("query").value;
  console.log(query)
  if (query.length > 0) {
      window.location.href = `json/${query}`;
  }
  return false;
}
