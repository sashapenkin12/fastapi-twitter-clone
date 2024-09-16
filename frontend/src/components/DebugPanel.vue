<template>
  <div
    v-if="isVisible"
    class="debug-panel"
  >
    <div class="debug-panel__current-key">
      <label>api-key текущего пользователя:</label>
      <label> {{ currentUserApiKey }}</label>
    </div>
    
  
    <input
      v-model="newApiKey"
      type="text"
    >
    <button
      class="debug-panel__set"
      @click="updateKey"
    >
      Установить новый api-key
    </button>

    <div class="debug-panel__pagination">
      <input
        :value="isPaginationEnabled"
        type="checkbox"
        @input="onPaginationChange"
      >
      <label>Пагинация</label>
    </div>

    <div
      v-if="isPaginationEnabled"
      class="debug-panel__pagination"
    >
      <label>Лимит</label>
      <input
        :value="paginationLimit"
        type="text"
        @input="onPaginationLimitChange"
      >
    </div>

    <button
      class="debug-panel__hide"
      @click="isVisible = false"
    >
      Скрыть
    </button>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      isVisible: true,
      newApiKey: '',
    }
  },
  computed: {
    ...mapState(['currentUserApiKey', 'isPaginationEnabled', 'paginationLimit']),
  },
  methods: {
    updateKey() {
      this.$store.commit('setCurrentUserApiKey', this.newApiKey);

      this.$store.dispatch('setLogOut');
      this.$router.push({path: '/login'})
    },

    onPaginationChange() {
      this.$store.commit('setIsPaginationEnabled', !this.isPaginationEnabled);
    },
    onPaginationLimitChange(to) {
      this.$store.commit('setPaginationLimit', to.target.value);
    }
  },
}
</script>


<style lang="scss">
.debug-panel {
  position: fixed;
  top: 0;
  right: 0;
  background: white;
  display: flex;
  flex-flow: column;
  z-index: 10;
  padding: 8px;

  &__pagination {
    display: flex;
    margin-top: 12px;
    align-items: center;
    
    input {
      margin-right: 4px;
    }
    label {
      margin-right: 4px;
    }
  }

  &__current-key {
    display: flex;
    flex-flow: column;
    margin-bottom: 12px;

    label {
      margin-top: 4px;
      
    }
  }

  &__set {
    margin-top: 4px;
  }

  &__hide {
    margin-top: 12px;
  }
}
</style>