<script>
    export let error  // 전달받은 오류
</script>

{#if typeof error.detail === 'string'}
    <div class="alert alert-danger" role="alert">{error.detail}</div>
{:else if typeof error.detail === 'object' && error.detail.length > 0 }
    <div class="alert alert-danger" role="alert">
        {#each error.detail as err, i}
        <div>
            <strong>{err.loc[1]}</strong> : {err.msg}
        </div>
        {/each}
    </div>
{/if}
