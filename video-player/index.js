(function() {
  var medias = {
    video: plyr.setup(".video",{
              // Output to console
              debug: false,
              clickToPlay: false,
              volume: 5
            }),
    audio: plyr.setup(".audio",{
              // Output to console
              debug: false,
              clickToPlay: false,
              controls: [],
              hideControls: true,
              volume: 5
            })},
  loadCount = 0,
  events = "play pause timeupdate seeking volumechange".split(/\s+/g); 
  
  // iterate both media sources
  for(var key in medias){
    medias[key][0].on("ready", function(){
      if(++loadCount == 2) {
        events.forEach(function(event){
          medias.video[0].on(event,function(){
            // Avoid overkill events, trigger timeupdate manually
            if (event === "timeupdate") {

              if (!medias[key][0].paused) {
                return;
              }
              medias.audio[0].emit("timeupdate");
              return;
            }

            if (event === "seeking") {
                medias.audio[0].seek(medias.video[0].getCurrentTime());
            }
            
            if (event === "volumechange") {
              medias.audio[0].setVolume(medias.video[0].getVolume() * 5);
            }

            if (event === "play" || event === "pause") {
              medias.audio[0][event]();
            }
          })
        })
      }
    })
  };
})();