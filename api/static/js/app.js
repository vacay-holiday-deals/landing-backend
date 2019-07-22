const container = document.getElementById("image-container");
const createNode = element => {
  return document.createElement(element);
};
const appendNode = (parent, el) => {
  return parent.appendChild(el);
};
const handleClick = id => {
  fetch(`http://localhost:5000/api/getimages/${id}`)
    .then(res => {
      return res.json();
    })
    .then(res => {
      let results = res;
      return results.map(result => {
        let div = createNode("div"),
          img = createNode("img"),
          i = createNode("i");
        img.src = result;
        appendNode(div, img);
        appendNode(div, i);
      });
    })

    .catch(error => console.log(error));
};
