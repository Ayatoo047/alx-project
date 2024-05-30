// scrollToConversationBottom();
console.log('slug')
let roomName = document.getElementById("bp-title").innerText;
// let username = username
let username = document.getElementById("userusername").innerText;

const threadScroll = document.getElementById("commentdiv");
const theMessage = document.getElementsByClassName("thread__details");
const commentList = document.getElementById('comment-list');
const textinput = document.getElementById("textinput");
const textForm = document.getElementById("textform");
const inputValue = textinput;
let ourdata = {};
let user_id = "";

function slugify(text) {
  return text
    .toString() // Ensure the input is a string
    .toLowerCase() // Convert to lowercase
    .trim() // Remove leading and trailing whitespace
    .replace(/\s+/g, "-") // Replace spaces with dashes
    .replace(/[^\w-]+/g, "") // Remove non-word characters except dashes
    .replace(/--+/g, "-"); // Replace consecutive dashes with a single dash
}

// Example usage:
const inputText = roomName;
const slug = slugify(inputText);
console.log(slug)

textForm.addEventListener("submit", (event) => {
    console.log('message')
//   if (socket.CLOSED){
//     console.log("reconnecting");
//     socket = new WebSocket(`ws://${window.location.host}/ws/chat/${slug}/`)
//   }
  event.preventDefault();
  const textInput = textinput.value;
  console.log(textInput);
  console.log(username);

  socket.send(
    JSON.stringify({
      message: textInput,
      sender: username,
    })
  );

//   if (socket.CLOSED) {
//     socket = new WebSocket(`ws://${window.location.host}/ws/chat/${slug}/`);

//     socket.send(
//       JSON.stringify({
//         message: textInput,
//         sender: username,
//       })
//     );
//   }

//   console.log(message,sender)
});

const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${slug}/`);
console.log("connected")

socket.onmessage = function (e) {
  // console.log('Server: ' + e.data);
  const { sender, message, create, } = JSON.parse(e.data);
  // appendThreadToThreadscroll(sender, message, 'https://randomuser.me/api/portraits/men/37.jpg');
    console.log(message)


    const newComment = document.createElement("div");
    newComment.classList.add("comment");
    console.log(message.id)
    newComment.id = `commentdiv-${message.id}`;
    newComment.innerHTML = `
                            <div class="comment__details">
                                <a href="#" style="margin-top: 10px;">${sender}</a>
                                <p class="comment__info" style=" margin-bottom: 1rem;">${message}</p>
                            </div>
                            <hr style="margin-bottom: 10px; ">
                        `;
    // Insert the new comment before the form container
    commentList.insertBefore(newComment, textForm.parentNode);
    console.log('done')
    // Optionally, clear the form input
    textForm.reset();
    // threadScroll.innerHTML += ` <div class="thread">
    //     <div class="thread__top">
    //         <div class="thread__author">
    //         <a href="${user_url}" class="thread__authorInfo">
    //             <div class="avatar avatar--small">
    //             <img src="https://randomuser.me/api/portraits/men/37.jpg" />
    //             </div>
    //             <span>@${sender}</span>
    //         </a>
    //         <span class="thread__date">${create}</span>
    //         </div>
            
    //         <a href="{% url 'deletemessage' message.id %}">
    //         <div class="thread__delete">
    //         <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
    //             <title>remove</title>
    //             <path
    //             d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"
    //             ></path>
    //         </svg>
    //         </div>
    //         </a>
    
    //     </div>
    //     <div class="thread__details">
    //         ${message}
    //     </div>
    //     </div>`;
  }
//   scrollToConversationBottom();
//   textinput.value = "";
;
