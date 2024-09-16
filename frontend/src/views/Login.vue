<template>
  <div class="login" />
</template>

<script>
import {login} from '@/services/api'
import { AvatarGenerator } from 'random-avatar-generator';
import { mapState } from 'vuex';


export default {
  name:'LoginView',
  data: function(){
    return {
      userInfo: {
        username: 'kaanersoy',
        password: 'password'
      },
      validationError: {
        username: false,
        password: false
      }
    }
  },
  computed: {
    ...mapState(['currentUserApiKey']),
  },
  mounted() {
    this.handleLogin();
  },
  methods:{
    handleLogin: async function(){
      try{
        const response = await login(this.userInfo, this.currentUserApiKey);
      
        if(!response.data.user){
          return
        }

        const { user } = response.data;

        const generator = new AvatarGenerator();
        const img = generator.generateRandomAvatar(user.id);
  
        this.$store.dispatch('setLoginInfo',
          {
            id: user.id,
            username: user.name,
            profile: {
              pic: img,
              pic_full: img,
              pic_cover: 'https://i.ibb.co/0G5ny1g/1500x500.jpg',
              description: '😎😎',
              nickname: user.name,
              name: user.name,
              website: 'https://cooldev.com'
            },
            account: {
              followingCount: user?.following?.length,
              followerCount: user?.followers?.length
            }
          })
        return this.$router.push('/')
      }catch(err) {
        this.$notification({
          type: 'error',
          message: 'Failed when authentication'
        })
      }
    },
    validateForm: function(){
      this.validationError.username = false
      this.validationError.password = false
      if(this.userInfo.username.length < 5){
        this.validationError.username = true
      }
      if(this.userInfo.password.length < 5){
        this.validationError.password = true
      }
    }
  }
}
</script>

<style lang="scss">
@import '@/assets/theme/colors.scss';
@import '@/assets/variables.scss';

.login{
  width: 400px;
  margin: 0 auto;
  margin-top: 20px;
  &-icon{
    width: 3rem;
    svg{
      width: 100%;
      fill: $color-blue;
    }
  }
  &-header{
    h2{
      font-size: 2rem;
      font-weight: black;
      color: #fff;
    }
  }
  &-form{
    margin-top: 2.5rem;
    & > * {
      margin-top: 2rem;
    }
    &-item{
      position: relative;
      & + .login-form-item{
        margin-top: 2.2rem;
      }
      input{
        display: block;
        width: 100%;
        font-size: 1.2rem;
        background-color: transparent;
        color: #fff;
        font-weight: bold;
        padding: .8rem 4px;
        border: 1px solid rgba($color: $color-dark-gray, $alpha: 0.3);
        &:focus{
          outline: none;
        }
        &:focus, &:valid{
          & ~ label{
            transform: translate(0, -3rem) scale(0.85);
            left: 0px;
          }
        }
      }
      label{
        position: absolute;
        left: 5px;
        top: 50%;
        color: #fff;
        transform: translate(0, -50%);
        transition: 200ms ease;
        user-select: none;
        pointer-events: none;
        -webkit-user-select: none;
      }
    }
  }
  &-submit{
    background-color: $color-blue;
    font-weight: bold;
    text-align: center;
    border-radius: 999px;
    padding: 1rem;
    color: #fff;
    cursor: pointer;
  }
  &-footer{
    text-align: center;
    color: $color-blue;
    span{
      &.dot{
        margin: 0 8px;
      }
    }
  }
}
@media screen and (max-width: $phone) {
  .login{
    width: 80%;
  }
}

</style>