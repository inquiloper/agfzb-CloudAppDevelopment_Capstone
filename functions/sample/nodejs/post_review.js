/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
    const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });
 
 
    try {
        const db = cloudant.db.use('reviews');
        const review  = params.review;
        const result = await db.insert({...review});
        return {
            code: 0,
            review
        }
    } catch (error) {
        return { error: error };
    }
 
}