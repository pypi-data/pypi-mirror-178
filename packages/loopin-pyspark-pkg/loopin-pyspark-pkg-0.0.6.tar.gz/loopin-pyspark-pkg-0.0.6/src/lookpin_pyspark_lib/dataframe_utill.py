def join_recommendation_data(recommendations, review_satisfaction_avg_df):
    return recommendations.join(review_satisfaction_avg_df, on='product_id')


def dataframe_select_columns(df, columns):
    return df.select(columns)


def show_recommend_list(join_data, member_id_list):
    join_data.filter('member_id in (' + ','.join(str(id) for id in member_id_list) + ')').sort('avg_satisfaction',
                                                                                               ascending=False).limit(
        10).show(10)
    