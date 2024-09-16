<template>
  <div class="home">
    <add-tweet @submit-click="handleTweetSubmit" />
    <hr class="gap">
    <div
      v-if="tweetData"
      class="tweet-wrapper"
    >
      <tweet
        v-for="tweet in tweetData"
        :key="tweet.id"
        :tweet-data="tweet"
        @delete-tweet="handleTweetDelete"
        @get-tweets="getTweets"
      />
    </div>

    <div class="home__pagination">
      <v-pagination
        v-if="isPaginationEnabled"
        v-model="page"
        :pages="Math.ceil(allTweetsCount/paginationLimit)"
        :range-size="1"
        active-color="#DCEDFF"
        @update:modelValue="onPaginate"
      />
    </div>
  </div>
</template>

<script>
import AddTweet from '@/components/AddTweet'
import Tweet from '@/components/Tweet'
import { getTweets, getTweetsWithPagination } from '@/services/api'
import { mapGetters, mapState } from 'vuex'
import VPagination from "@hennge/vue3-pagination";
import "@hennge/vue3-pagination/dist/vue3-pagination.css";

export default {
  components: {
    AddTweet,
    Tweet,
    VPagination,
  },
  data: function(){
    return{
      tweetData: [],
      page: 1,
      allTweetsCount: 10,
    }
  },
  computed: {
    ...mapGetters(['getMe']),

    ...mapState(['isPaginationEnabled', 'paginationLimit'])
  },
  watch: {
    isPaginationEnabled() {
      this.getTweets();
    }
  },
  mounted: async function() {
    this.getTweets()
  },
  methods: {
    onPaginate() {
      this.getTweets();
    },

    async handleTweetSubmit(){
      try{
        await this.getTweets();
      }catch(err){
        this.$notification({
          type: 'error',
          message: 'Error in send tweet'
        })
      }
    },
    getTweets: async function(){
      let response;
  
      if (this.isPaginationEnabled) {
        const allTweetsResponse = await getTweets();
        this.allTweetsCount  = allTweetsResponse?.data?.tweets?.length;
        response = await getTweetsWithPagination(this.page, this.paginationLimit);
      } else {
        response = await getTweets();
      }
      
      this.tweetData = response?.data?.tweets;
    },
    async handleTweetDelete(){
      this.handleTweetSubmit()
    }
  }
}
</script>

<style lang="scss">
@import '@/assets/theme/colors.scss';

.home {
  &__pagination {
    display: flex;
    justify-content: center;
  }
  padding-bottom: 16px;
}

.Pagianation {
  .Page {
    width: 36px;
    height: 36px;
    font-size: 16px;
  }
}

hr.gap{
  background-color: $hr-color;
  padding: 4px 0;
  margin: 0;
  border: none;
}
</style>