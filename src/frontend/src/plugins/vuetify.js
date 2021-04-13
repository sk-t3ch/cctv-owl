import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: true,
        options: { customProperties: true },
        themes: {
          dark: {
            primary: '#191923',
            secondary:'#3F6634',
            accent: '#04F06A',
            error: '#9F84BD',
          },
        },
      },
});
