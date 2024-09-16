<template>
  <div
    class="profile"
  >
    <profile-header
      :id="userId"
      :following="following"
      :followers="followers"
      :name="name"
      @refresh="getData"
    />
    <profile-body />
    <EditProfilePopup v-if="getEditProfileStatus" />
  </div>
</template>

<script>
import ProfileBody from '@/components/Profile/ProfileBody'
import ProfileHeader from '@/components/Profile/ProfileHeader'
import EditProfilePopup from '@/components/EditProfilePopup'
import { getUserInfo } from '@/services/api';

import { mapGetters } from 'vuex';

export default {
  name: 'ProfileView',
  components:{
    ProfileBody,
    ProfileHeader,
    EditProfilePopup
  },
  data(){
    return{
      userId: null,
      following: [],
      followers: [],
      name: '',
    }
  },
  computed:{
    ...mapGetters(['getMyProfileId', "getEditProfileStatus"]),
  },
  async mounted(){
    this.getData();
  },
  methods: {
    async getData(){
      const { profileId } = this.$route?.params;
      const { data } = await getUserInfo(profileId)
      this.userId = data?.user.id;
      this.following = data?.user.following;
      this.followers = data?.user.followers;
      this.name = data?.user.name;
    }
  }
}
</script>

<style lang="scss">
@import '@/assets/theme/colors.scss';

.profile{
  .profile-cover-pic{
    img{
      width: 100%;
    }
  }
  &-header{
    padding: 1rem;
  }
}
</style>