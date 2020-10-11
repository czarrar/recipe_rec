// ----------
// # Functions
// -----------

// Sprintf
if (!String.format) {
    String.format = function (format) {
        var args = Array.prototype.slice.call(arguments, 1);
        return format.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
        ;
        });
    };
}

// Range function
function range(start, end) {
    return (new Array(end - start + 1)).fill(undefined).map((_, i) => i + start);
}



/****
* GENERAL STUFF
****/

var trials = [];

var fix_break = {
    type: 'html-keyboard-response',
    data: { ttype: 'fix' },
    stimulus: '<div style="font-size:3em">+</div>',
    choices: jsPsych.NO_KEYS,
    stimulus_duration: 1000,
    trial_duration: 1000,
    response_ends_trial: false
}

var fix_trial = {
    type: 'html-keyboard-response',
    data: { ttype: 'fix' },
    stimulus: '<div style="font-size:3em">+</div>',
    choices: jsPsych.NO_KEYS,
    stimulus_duration: 500,
    trial_duration: 500,
    response_ends_trial: false
}




/***************************************
# MAIN PART
***************************************/


// #------------------------
// ## Learning Phase - Values
// #------------------------

var choice_start = {
	type: 'html-keyboard-response',
	data: { ttype: 'block' },
	stimulus: String.format('<p class="title">Training: Value of Paintings</b></p>\
	<p class="instruct2">You will see the same paintings as before but will now learn about their value.</p>\
	<p class="instruct2">Pairs of paintings from the same or different galleries will be shown and you must choose the painting of higher value. You will be given feedback on the value of the chosen painting. You can use your memory of a paintings value and its gallery to guide your choices. Some paintings and some galleries will be worth more than others.</p>\
	<p class="instruct2">Press "j" to select the painting on the left and "k" to select the painting on the right. You will have up to 5 seconds to make your choice and will then be shown the value for 1.5s.</p>\
  <p class="instruct">Press "j" or "k" to continue.'),
	choices: ['j','k']
};
trials.push(choice_start);


// #--------------
// ### Show Trials
// #--------------

// Participants will see paintings and pairs and decide on which is the most valuable one
// I'm not sure if I'd want repeat trials. I think I probably would want that.

choice_pairs = [
    {
      left: {image: 'static/images/6669.jpg', name: 'Jalapeno Cheese Bread',
        ingredients: 'all-purpose flour, shredded Cheddar cheese, minced jalapeno peppers, white sugar, salt, hot water, active dry yeast, vegetable oil' },
      right: {image: 'static/images/7313.jpg', name: 'Brown Sugar Cake',
          ingredients: 'packed brown sugar, butter, sour cream, baking soda, all-purpose flour, baking powder, ground nutmeg, ground cinnamon, raisins, eggs'}
    },
    {
      left: {image: 'static/images/233786.jpg', name: 'Mediterranean Turkey Pasta Salad',
        ingredients: 'olive oil, red wine vinegar, minced fresh garlic, dried oregano leaves, Butterball® Golden Oven Roasted Turkey Breast sliced thick and cubed, cooked penne pasta, pitted kalamata olives drained chopped, pint grape tomatoes halved, crumbled feta cheese, spring lettuce mix, chopped Italian parsley, thinly sliced red onions'},
      right: {image: 'static/images/234531.jpg', name: 'Bethanys Frito Pie',
          ingredients: 'corn chips (such as Fritos®), shredded Cheddar cheese, chopped onion, prepared chili'}
    }
];

for (var i = 0; i < choice_pairs.length; i++) {
  var pair = choice_pairs[i];

  // Get the recipe image paths
  var stim_l = pair.left.image;
  var stim_r = pair.right.image;

  // Get the recipe names

  // Get the recipe ingredients

  // ##
  // ### Show Stimuli
  // ##
  var learn_trial_a = {
  	type: 'html-keyboard-response',
  	data: { ttype: 'stimuli',
            trialnum: i,
            stim_left: pair.left.image, stim_right: pair.right.image,
            name_left: pair.left.name, name_right: pair.right.name,
            ingredient_left: pair.left.ingredients, ingredient_right: pair.right.ingredients
          },
  	stimulus: String.format(
      '<div>\
        <div id="rbox"><img id="rstim" src="{0}" /><p>{2}</p></div>\
        <div id="rbox"><img id="rstim" src="{1}" /><p>{3}</p></div>\
        <p class="subtitle2">Left (j) --------------------------- Right (k)</p>\
       </div>',
      pair.left.image, pair.right.image,
      pair.ingredient_left, pair.ingredient_right
    ),
  	choices: ['j', 'k'],
  	stimulus_duration: 5000,
  	trial_duration: 5000,
  	response_ends_trial: true,
    on_finish: function(data) {
      // Update the total value
      if (data.key_press == null) {
        //console.log('no response');
        return;
      }
    }
  };
  trials.push(learn_trial_a);


  // ##
  // ### Indicate selection
  // ##
  var learn_trial_b = {
    type: 'html-keyboard-response',
    data: { ttype: 'feedback' },
    stimulus: function() {
      var last_trial = jsPsych.data.get().last(1).values()[0];
      if (last_trial.key_press == jsPsych.pluginAPI.convertKeyCharacterToKeyCode('j')) {
        return(String.format(
          '<div>\
            <div id="rbox_selected">\
              <img id="rstim" src="{0}" />\
            </div>\
            <div id="rbox">\
              <img id="rstim" src="{1}" />\
            </div>\
            <p class="subtitle2">&nbsp;</p>\
           </div>',
          last_trial.stim_left, last_trial.stim_right));
      } else if (last_trial.key_press == jsPsych.pluginAPI.convertKeyCharacterToKeyCode('k')) {
        return(String.format(
          '<div>\
            <div id="rbox">\
              <img id="rstim" src="{0}" />\
            </div>\
            <div id="rbox_selected">\
              <img id="rstim" src="{1}" />\
            </div>\
            <p class="subtitle2">&nbsp;</p>\
           </div>',
          last_trial.stim_left, last_trial.stim_right));
      } else {
        return("<div style='font-size:40px'>Too Slow<br /><br />(Press j=left / k=right)</div>");
      }
    },
    choices: jsPsych.NO_KEYS,
    stimulus_duration: 1000,
    trial_duration: 1000,
    response_ends_trial: false,
  }
  trials.push(learn_trial_b);


  // ##
  // ### Fixation
  // ##
  var learn_trial_c = {
      type: 'html-keyboard-response',
      data: { ttype: 'fix' },
      stimulus: '<div><div class="fix">+</div><p class="subtitle2">&nbsp;</p></div>',
      choices: jsPsych.NO_KEYS,
      stimulus_duration: 1000,
      trial_duration: 1000,
      response_ends_trial: false
  }
  trials.push(learn_trial_c);
}

function saveData(data){
   $.ajax({
      type:'post',
      cache: false,
      url: 'choose_results',
      contentType: "application/json",
      data: data,
      success: function(output) { console.log(output); }
   });
}

var save_data = {
  type: 'call-function',
  func: function() {
    saveData(jsPsych.data.get().json());
  }
}
trials.push(save_data);







jsPsych.init({
    timeline: trials,
    //preload_images: all_imgs,
    show_progress_bar: true, //, should i include this?

    on_trial_finish: function(data) {
        console.log('A trial just ended.');
        console.log(JSON.stringify(data));
    }
});
