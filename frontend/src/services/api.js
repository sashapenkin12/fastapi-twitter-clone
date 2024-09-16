/* eslint-disable no-unused-vars */
import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import store from '@/store'
import {userOneAuthInfo, users, tweets, trends} from './mockdata'

// const mock = new MockAdapter(axios, {delayResponse: 250});
// mock.onPost("/auth", userOneAuthInfo).reply(200, {user: users[0]});
// mock.onGet("/tweets").reply(200, {tweets});
// mock.onGet("/trends").reply(200, {trends});
// mock.onPost("/tweets").reply(function (config) {
//   tweets.unshift(JSON.parse(config.data))
//   return [200, tweets]
// });
// mock.onPost("/medias").reply(200, { media_id: 1 });

// mock.onPatch("/tweets").reply(function (config) {
//   const request = JSON.parse(config.data)
  
//   const requestedTweet = tweets.find(twt => twt.id == request.id);
//   const requestedIndex = tweets.indexOf(requestedTweet);

//   tweets[requestedIndex].content = request.content;

//   return [200, {
//     message: 'Tweet is editted succesfully',
//     id: request.id
//   }]
// });

// mock.onDelete("/tweets").reply(function (config) {
//   const tweetId = config.tweetId

//   const findedTweet = tweets.find(twt => twt.id == tweetId)
//   const indexOfTweet = tweets.indexOf(findedTweet)

//   tweets.splice(indexOfTweet, 1);

//   return [200, {
//     message: 'Deleted successfully',
//     tweetId
//   }]
// });

// mock.onPost("/me", {id: users[0].id}).reply(200, users[0]);

// mock.onGet(`/tweets/${users[0].id}`).reply(function() {
//   return [200, {
//     tweets: tweets.filter(twt => twt.author.id == users[0].id)
//   }]
// });

// mock.onPut('/me').reply(function (config) {
//   const request = JSON.parse(config.data)

//   const me = users.find(usr => usr.id == store.getters.getMyProfileId)
//   const myIndex = users.indexOf(me);

//   Object.keys(request).map(key => {
//     users[myIndex].profile[key] = request[key]
//   })

//   const response = {
//     message: 'Editted succesfully!',
//     updatedProfile: users[myIndex].profile
//   }
//   return [200, response]
// })


export async function login(body, apiToken){
  return request({type: 'get', path: '/api/users/me'});
  // return Promise.resolve({ data: { user: users.find((user) => user.api_token === apiToken)}})
}

export async function getUserInfo(userId){
  return request({type: 'get', path: `/api/users/${userId}`});
  // return Promise.resolve({ data: { user: users.find((user) => user.id == userId)}})
}

export async function followUser(userId) {
  return request({type: 'post', path: `/api/users/${userId}/follow`})
}

export async function unfollowUser(userId) {
  return request({type: 'delete', path: `/api/users/${userId}/follow`})
}

export async function getTweets(){
  return request({type: 'get', path: '/api/tweets'})
}

export async function getTweetsWithPagination(offset, limit){
  return request({type: 'get', path: `/api/tweets?offset=${offset}&limit=${limit}`})
}

export async function getTrends(){
  return request({type: 'get', path: '/trends'})
}

export async function getMe(body){
  return request({type: 'post', path: '/me', body})
}

export async function uploadTweet(body){
  return request({type: 'post', path: '/api/tweets', body})
}

export async function deleteTweet(tweetId){
  return request({type: 'delete', path: `/api/tweets/${tweetId}`})
}

export async function updateTweet(body){
  return request({type: 'patch', path: '/tweets', body})
}

export async function getUsersTweets(body){
  return request({type: 'get', path: `/tweets/${body.id}`})
}

export async function setProfileInfo(body){
  return request({type: 'put', path: `/me`, body})
}

export async function uploadMedia(body) {
  return request({type: 'post', path: `/api/medias`, body})
}

export async function likeTweet(tweetId) {
  return request({type: 'post', path: `/api/tweets/${tweetId}/likes`})
}

export async function dislikeTweet(tweetId) {
  return request({type: 'delete', path: `/api/tweets/${tweetId}/likes`})
}




async function request(settings){
  store.commit("setLoadingStatus", true)
  try {
    // axios.defaults.baseURL = 'http://localhost:8090/'
    axios.defaults.baseURL = '/'
    axios.defaults.headers.common['api-key'] = store.state?.currentUserApiKey

    if(settings.body){
      const response = await axios[settings.type](settings.path, settings.body);
      store.commit("setLoadingStatus", false)
      return response;
    }
    const response = await axios[settings.type](settings.path);
    store.commit("setLoadingStatus", false)
    return response;
  }catch(error) {
    console.log(error);
    store.commit("setLoadingStatus", false)
    throw new Error(error)
  }
}