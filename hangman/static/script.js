const canvas = document.getElementById('hangman');
const context = canvas.getContext("2d");
const guesses = document.getElementById("guesses").innerHTML

clearCanvas = () => {
  context.clearRect(0, 0, canvas.width, canvas.height)
}

Draw = (part) => {
   switch (part) {
      case 'start':
        break;

      case 'gallows' :
        context.strokeStyle = '#966F33';
        context.lineWidth = 10; 
        context.beginPath();
        context.moveTo(180, 225);
        context.lineTo(0, 225);
        context.moveTo(40, 225);
        context.lineTo(40, 5);
        context.lineTo(100, 5);
        context.lineTo(100, 25);
        context.moveTo(0, 225);
        context.lineTo(40, 185);
        context.lineTo(80, 225);
        context.moveTo(40, 45);
        context.lineTo(80, 5);
        context.stroke();
        break;

      case 'head':
        context.lineWidth = 5;
        context.beginPath();
        context.arc(100, 50, 25, 0, Math.PI*2, true);
        context.closePath();
        context.stroke();
        break;
      
      case 'body':
        context.beginPath();
        context.moveTo(100, 75);
        context.lineTo(100, 140);
        context.stroke();
        break;

      case 'rightHarm':
        context.beginPath();
        context.moveTo(100, 85);
        context.lineTo(60, 100);
        context.stroke();
        break;

      case 'leftHarm':
        context.beginPath();
        context.moveTo(100, 85);
        context.lineTo(140, 100);
        context.stroke();
        break;

      case 'rightLeg':
        context.beginPath();
        context.moveTo(100, 140);
        context.lineTo(80, 190);
        context.stroke();
        break;

      case 'feet':
         context.beginPath();
         context.moveTo(82, 190);
         context.lineTo(70, 185);
         context.moveTo(122, 190);
         context.lineTo(135, 185);
         context.stroke();
      break;

      case 'leftLeg':
        context.beginPath();
        context.moveTo(100, 140);
        context.lineTo(125, 190);
        context.stroke();
      break;

   } 
}

const draws = [
  'start', 
  'gallows', 
   'head', 
   'body', 
   'rightHarm', 
   'leftHarm',
   'rightLeg',
   'leftLeg',
   'feet',
]

for (var i = 0; i <= (8 - guesses); i++) {
  Draw(draws[i])
}
//Draw(draws[8 - guesses])
console.log(guesses)
// var step = 0;

/*
const next = document.getElementById('next')

next.addEventListener('click', function() {
  Draw(draws[step++])
  if (undefined === draws[step]) this.disabled = true;
});

document.getElementById('reset').addEventListener('click', function() {
  clearCanvas()
  step = 0
  next.disabled = false
})
*/
