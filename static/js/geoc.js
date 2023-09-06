let map;
let marker;
let geocoder;
let responseDiv;
let response;

let popup, Popup;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: { lat: 42.6410428, lng: -95.2097352},
    mapTypeControl: false,
  });
  geocoder = new google.maps.Geocoder();

  const inputText = document.createElement("input");

  inputText.type = "text";
  inputText.setAttribute('id','location_input');
  inputText.placeholder = "Enter a location";

  const submitButton = document.createElement("input");

  submitButton.type = "button";
  submitButton.value = "Search";
  submitButton.classList.add("button", "button-primary");

  const clearButton = document.createElement("input");

  clearButton.type = "button";
  clearButton.value = "Clear";
  clearButton.classList.add("button", "button-secondary");
  response = document.createElement("pre");
  response.id = "response";
  response.innerText = "";
  responseDiv = document.createElement("div");
  responseDiv.id = "response-container";
  responseDiv.appendChild(response);

  const instructionsElement = document.createElement("p");

  instructionsElement.id = "instructions";
  instructionsElement.innerHTML =
    "<strong>Instructions</strong>: Enter location name and press Search button";
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(inputText);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(submitButton);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(clearButton);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(instructionsElement);
  map.controls[google.maps.ControlPosition.LEFT_TOP].push(responseDiv);
  marker = new google.maps.Marker({
    map,
  }); 
  map.addListener("click", (e) => {
    geocode({ location: e.latLng }); 
    //alert(e.latLng);
  });
  submitButton.addEventListener("click", () =>
    post_loc_input(inputText.value)
  );
  clearButton.addEventListener("click", () => {
    clear();
  });
  clear();

  /** 
   * A customized popup on the map.
   */
  class Popup extends google.maps.OverlayView {
    position;
    containerDiv;
    constructor(position, content) {
      super();
      this.position = position;
      content.classList.add("popup-bubble");

      // This zero-height div is positioned at the bottom of the bubble.
      const bubbleAnchor = document.createElement("div");

      bubbleAnchor.classList.add("popup-bubble-anchor");
      bubbleAnchor.appendChild(content);
      // This zero-height div is positioned at the bottom of the tip.
      this.containerDiv = document.createElement("div");
      this.containerDiv.classList.add("popup-container");
      this.containerDiv.appendChild(bubbleAnchor);
      // Optionally stop clicks, etc., from bubbling up to the map.
      Popup.preventMapHitsAndGesturesFrom(this.containerDiv);
    }   
    /** Called when the popup is added to the map. */
    onAdd() {
      this.getPanes().floatPane.appendChild(this.containerDiv);
    }   
    /** Called when the popup is removed from the map. */
    onRemove() {
      if (this.containerDiv.parentElement) {
        this.containerDiv.parentElement.removeChild(this.containerDiv);
      }   
    }   
    /** Called each frame when the popup needs to draw itself. */
    draw() {
      const divPosition = this.getProjection().fromLatLngToDivPixel(
        this.position
      );  
      // Hide the popup when it is far out of view.
      const display =
        Math.abs(divPosition.x) < 4000 && Math.abs(divPosition.y) < 4000
          ? "block"
          : "none";

      if (display === "block") {
        this.containerDiv.style.left = divPosition.x + "px";
        this.containerDiv.style.top = divPosition.y + "px";
      }

      if (this.containerDiv.style.display !== display) {
        this.containerDiv.style.display = display;
      }
    }
  }
}

function post_loc_input(loc_name){
    /** 
   * A customized popup on the map.
   */
  class Popup extends google.maps.OverlayView {
    position;
    containerDiv;
    constructor(position, content) {
      super();
      this.position = position;
      content.classList.add("popup-bubble");

      // This zero-height div is positioned at the bottom of the bubble.
      const bubbleAnchor = document.createElement("div");

      bubbleAnchor.classList.add("popup-bubble-anchor");
      bubbleAnchor.appendChild(content);
      // This zero-height div is positioned at the bottom of the tip.
      this.containerDiv = document.createElement("div");
      this.containerDiv.classList.add("popup-container");
      this.containerDiv.appendChild(bubbleAnchor);
      // Optionally stop clicks, etc., from bubbling up to the map.
      Popup.preventMapHitsAndGesturesFrom(this.containerDiv);
    }   
    /** Called when the popup is added to the map. */
    onAdd() {
      this.getPanes().floatPane.appendChild(this.containerDiv);
    }   
    /** Called when the popup is removed from the map. */
    onRemove() {
      if (this.containerDiv.parentElement) {
        this.containerDiv.parentElement.removeChild(this.containerDiv);
      }   
    }   
    /** Called each frame when the popup needs to draw itself. */
    draw() {
      const divPosition = this.getProjection().fromLatLngToDivPixel(
        this.position
      );  
      // Hide the popup when it is far out of view.
      const display =
        Math.abs(divPosition.x) < 4000 && Math.abs(divPosition.y) < 4000
          ? "block"
          : "none";

      if (display === "block") {
        this.containerDiv.style.left = divPosition.x + "px";
        this.containerDiv.style.top = divPosition.y + "px";
      }   

      if (this.containerDiv.style.display !== display) {
        this.containerDiv.style.display = display;
      }
    }
  }

  clear();
  initMap();
  data={"location": loc_name};
  json = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/loc_input",
    data: json,
    contentType: "application/json",
    dataType: 'json',
    success: function(results) {
      let center_lat, center_lon;
      console.log(results)
      for (const post in results){
          //console.log(post);
          //console.log(results[post]);
          //console.log(results[post]['shortcode']);
          const custom_popup = document.createElement("div");
          custom_popup.id = "post"+post;
          const link_wrap = document.createElement("a");
          link_wrap.setAttribute('href', 'https://www.instagram.com/p/'+results[post]['shortcode']+'/');
          link_wrap.target = "_blank";
          var image = document.createElement("img");
          image.src = './static/img/'+loc_name+'/'+results[post]['timestamp']+'/'+results[post]['shortcode']+'.jpg';
          image.width = "100";
          image.height = "100";
          link_wrap.appendChild(image);
          custom_popup.appendChild(link_wrap);

          const _posts = document.getElementById("posts");
          _posts.appendChild(custom_popup);

          const popup1 = new Popup(
            new google.maps.LatLng(results[post]['lat'], results[post]['lon']),
            document.getElementById("post"+post)
          );
          popup1.setMap(map);
          center_lat = results[post]['lat'];
          center_lon = results[post]['lon'];
      }
      map.setCenter({lat: parseFloat(center_lat), lng: parseFloat(center_lon) });
    },
    error: function(msg) {
      console.log("error");
    }
  });
}

function clear() {
  const loc_input = document.getElementById('location_input');
  //loc_input.value = null;
  $('#location_input').val("");
  const _posts = document.getElementById("posts");
  while (_posts.firstChild){
    _posts.removeChild(_posts.firstChild)
  }
  marker.setMap(null);
  responseDiv.style.display = "none";
}

function geocode(request) {
  clear();
  geocoder
    .geocode(request)
    .then((result) => {
      const { results } = result;

      map.setCenter(results[0].geometry.location);
      //alert(results[0].geometry.location);
      //marker.setPosition(results[0].geometry.location);
      //marker.setMap(map);
      //responseDiv.style.display = "block";
      //response.innerText = JSON.stringify(result, null, 2);
      //alert(response.innerText);
      return results;
    })
    .catch((e) => {
      alert("error: " + e);
    });
}

