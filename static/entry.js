const feedTypeButton = document.getElementById("feed-type")
feedTypeButton.addEventListener(
  'click',
  () => {
    const next = 'atomjson'.replace(feedTypeButton.value, '')
    feedTypeButton.value = next
    feedTypeButton.textContent = next
  }
)

document.getElementById("query").addEventListener(
  'keypress',
  (event) => {
    // Handle 'enter' keypresses.
    if (event.keyCode === 13) {
      event.preventDefault();
      redirectToFeed(feedTypeButton.value);
    }
  }
)

function redirectToFeed(feedType) {
  const query = document.getElementById("query").value;
  console.log(query)
  if (query.length > 0) {
      window.location.href = `${feedType}/${query}`;
  }
  return false;
}
