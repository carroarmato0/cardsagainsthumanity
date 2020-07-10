% rebase('base.tpl', title="CAH - DeckManager", stylesheets=stylesheets, scripts=scripts)

    <hr/>
    <section id="controls">
        <form action="/api/v1/decks/" method="post">
            <label for="fname">Name:</label>
            <input type="text" id="fname" name="fname" value="">
            <label for="fdescription">Description:</label>
            <input type="text" id="fdescription" name="fdescription" value="">
            <label for="flang">Language:</label>
            <input type="text" id="flang" name="flang" size="1" value="en">
            <input type="submit" value="Add" />
        </form>
    </section>
    <hr/>

    <main id="app">
        <span class="error" v-if="notFound">There are no Decks found :(</span>
        <ul class="decks">
            <li class="deck" v-for="deck in decks" :key="deck._id">
                <a v-bind:href="'/decks/' + deck._id.$oid">
                    <article>
                        <p class="content">{{ '{{ deck.name }}' }}</p>
                        <ul class="modifiers">
                            <li>Language: {{ '{{ deck.lang }}' }}</li>
                            <li>Cards: {{ '{{ deck.cards.length }}' }}</li>
                        </ul>
                    </article>
                </a>
            </li>
        </ul>
    </main>

    <script>
        new Vue({
          el: '#app',
          data () {
            return {
              decks: null,
              notFound: true
            }
          },
          mounted () {
            axios
              .get('/api/v1/decks/')
              .then(response => (
                this.decks = response.data,
                this.notFound = false
              ))
          }
        })
    </script>