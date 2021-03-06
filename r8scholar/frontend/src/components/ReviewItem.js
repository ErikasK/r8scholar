import React, { Component } from "react";
import { Card, CardHeader, CardBody, CardTitle, CardText, ListGroupItem, Button, Row, Col, Label, CardFooter, Progress } from "reactstrap";
import StarRatings from "react-star-ratings";
import ReportForm from "./ReportReviewForm";
import EditForm from "./EditReviewForm";
import DeleteForm from "./DeleteReviewForm";
import CommentForm from "./CommentForm";
import { MdThumbUp, MdThumbDown } from "react-icons/md";
import axiosInstance from "../axiosApi";
import cookie, { setRawCookie } from "react-cookies";

const reviewTitle = {
    color: "black",
    fontSize: "25px",
    fontWeight: "300",
};

const tagStyle = {
    borderRadius: "15px",
    height: "25px",
    backgroundColor: "#fbfcfc",
    color: "#000",
    width: "max-content",
    marginRight: "1%",
    marginBottom: "1%",
};

//props contains object called reviewItem containing
/*
        -Title {this.props.reviewItem.title}
        -Content {this.props.reviewItem.content}
        -Rating rating={this.props.reviewItem.rating}
        -User {this.props.reviewItem.nickname}
        -reviewID {this.props.reviewItem.reviewID}
        -Comments (object)
        */
//second props contains a boolean value which determines of the edit button should be there
//this.props.isOwner
export default class ReviewItem extends Component {
    //props is going to consist of the review item passed by the course
    constructor(props) {
        super(props);
        this.vote = this.vote.bind(this);
    }

    async vote(up) {
        try {
            response = await axiosInstance.post("/thumbs-review/", {
                review_id: this.props.reviewItem.review_id,
                email: cookie.load("email"),
                up_or_down: up ? "up" : "down",
            });
            return response.status;
        } catch (error) {
            console.log(error.message);
        }
    }

    //the JSX that is rendered when this file is imported as a component
    render() {
        console.log("reivewItem", this.props);
        return (
            <div className="App">
                {/* container (card )which includes a title section + rating and a content section + button to see comments */}
                <Card>
                    <CardHeader>
                        <Row>
                            <Col className="col-md-7" align="left">
                                <p style={reviewTitle}>{this.props.reviewItem.title}</p>
                            </Col>
                            {/* If user is logged in show edit review and delete review buttons, if logged out show up/down votes */}
                            {this.props.isOwner ? (
                                <Col className="col-md-5" style={{ marginLeft: "auto", minWidth: "max-content", maxWidth: "200px" }}>
                                    <EditForm type={this.props.type} review={this.props.reviewItem} />
                                    <DeleteForm review={this.props.reviewItem} />
                                </Col>
                            ) : (
                                <Col className="col-md-3" align="right" style={{ marginLeft: "auto", minWidth: "max-content", maxWidth: "180px" }}>
                                    <Button
                                        style={{ borderRadius: "45%", borderColor: "#f1f1ee", backgroundColor: "#f1f1ee", color: "#77dd77", float: "left" }}
                                        className="btn-round"
                                        type="button"
                                        id="upvote"
                                        onClick={() => this.vote(true)}
                                    >
                                        <MdThumbUp size="20px" />
                                    </Button>
                                    <Button
                                        style={{ borderRadius: "45%", borderColor: "#f1f1ee", backgroundColor: "#f1f1ee", color: "#f5593d" }}
                                        className="btn-round"
                                        type="button"
                                        id="downvote"
                                        onClick={() => this.vote(false)}
                                    >
                                        <MdThumbDown size="20px" />
                                    </Button>
                                    <Progress multi style={{ marginTop: "5%" }}>
                                        <Progress var color="green" value={(this.props.reviewItem.thumbs_up / (this.props.reviewItem.thumbs_down + this.props.reviewItem.thumbs_up)) * 100} />
                                        <Progress bar color="red" value={(this.props.reviewItem.thumbs_down / (this.props.reviewItem.thumbs_down + this.props.reviewItem.thumbs_up)) * 100} />
                                    </Progress>
                                </Col>
                            )}
                        </Row>
                    </CardHeader>
                    <CardBody>
                        <CardTitle style={{ display: "flex", flexWrap: "wrap-reverse" }}>
                            <h6 style={{ marginRight: "1%" }}>{this.props.reviewItem.nickname}</h6>
                            {this.props.reviewItem.would_take_again ? (
                                <h6>recommends the {this.props.reviewItem.review_type} </h6>
                            ) : (
                                <h6>does not recommend the {this.props.reviewItem.review_type}</h6>
                            )}
                            <div style={{ marginLeft: "auto" }}>
                                <StarRatings rating={this.props.reviewItem.rating} starDimension="30px" starSpacing="10px" starRatedColor="#3498db" numberOfStars={5} name="instructorRating" />
                            </div>
                        </CardTitle>
                        <CardText>
                            <h5>{this.props.reviewItem.content}</h5>
                        </CardText>
                        <CardFooter>
                            {this.props.reviewItem.tag_1 != null ? (
                                <>
                                    <Button style={tagStyle} disabled>
                                        <p style={{ marginTop: "-7px" }}>{this.props.reviewItem.tag_1}</p>
                                    </Button>
                                    {this.props.reviewItem.tag_2 != null ? (
                                        <>
                                            <Button style={tagStyle} disabled>
                                                <p style={{ marginTop: "-7px" }}>{this.props.reviewItem.tag_2}</p>
                                            </Button>
                                            {this.props.reviewItem.tag_3 != null ? (
                                                <Button style={tagStyle} disabled>
                                                    <p style={{ marginTop: "-7px" }}>{this.props.reviewItem.tag_3}</p>
                                                </Button>
                                            ) : null}
                                        </>
                                    ) : null}
                                </>
                            ) : null}
                        </CardFooter>
                    </CardBody>
                    <ListGroupItem>
                        <Row>
                            <Col align="left">
                                <CommentForm review={this.props.reviewItem} currentUser={this.props.currentUser} />
                            </Col>
                            <Col align="right">
                                <p style={{ display: "inline", marginRight: "5%", verticalAlign: "middle" }}>{this.props.reviewItem.date_created}</p>
                                <ReportForm reviewID={this.props.reviewItem.review_id} />
                            </Col>
                        </Row>
                    </ListGroupItem>
                </Card>
            </div>
        );
    }
}
