
let actor_movies = {};
let current_name='';

// var x = $.csv.toObjects('tmdb_5000_credits.csv');
// console.log(x)
let get_actors = credits => {
    let actor_names = []
    let actor_movies = {}
    for (var c of credits){
        let credit = JSON.parse(c['cast'])
        for (p of credit){
            actor_names.push(p['name'])
            if (!actor_movies.hasOwnProperty(p['name'])){
                actor_movies[p['name']]=[]
            }
            actor_movies[p['name']].push(c['title'])
        }

    }
    return [actor_names, actor_movies]
};

let shuffleWord = (word) => {
    const shuffled= word.split('').sort().join('')
    return shuffled
};

$( "#answer" ).click(function() {
    $("#name").append(current_name);
});

$( "#hint" ).click(function() {
    $("#movies").append('\n<br/>'+actor_movies[current_name][Date.now()%actor_movies[current_name].length]);
});

$( "#next" ).click(function() {  
    current_name = randomActor(actor_names)
    playRound(current_name,actor_movies,false)
});

let playRound = (name, actor_movies, easy=False) =>{
    let points=0
    let shfl = shuffleWord(name)
    if (!easy){
        shfl=shfl.toLowerCase()
    }
    $("#name").text(shfl);
    $("#movies").text(actor_movies[name][Date.now()%actor_movies[name].length]);
};

let randomActor = (actor_names) =>{
    return actor_names[Math.round(Date.now()/(60*200))%actor_names.length]
}

let playGame = actor_movies =>{
    console.log('actor_names loaded',actor_movies)
    // let [actor_names, actor_movies] = get_actors(data)
    actor_names = Object.keys(actor_movies)
    console.log('actors loaded',actor_names)
    current_name = randomActor(actor_names)
    playRound(current_name,actor_movies,false)
};

let loadData= () =>{
    $.getJSON( "./actor_movies_200.json", function( data ) {
        actor_movies = data;
        playGame(actor_movies);
        
      });
};

loadData();