import React from "react";
import { Button, Input, Modal, FormGroup, Label } from "reactstrap";
import { BsFillExclamationCircleFill } from "react-icons/bs";
import axiosInstance from "../axiosApi";

function ReportCommentForm(props) {
    const [loginModal, setLoginModal] = React.useState(false);
    const [content, setContent] = React.useState("");
    const [selected, setSelected] = React.useState("");
    const reasons = ["It contains offensive content", "It is clearly untrue", "Does not contain relevant information to this review"];

    const handlePress = (e) => {
        setSelected(e.target.id);
    };

    const handleChange = (e) => {
        setContent(e.target.value);
    };

    const submit = async () => {
        try {
            let response = await axiosInstance.post("/report-comment/", {
                comment_id: props.comment_id, //insert the comment ID
                report_description: selected === "4" ? content : reasons[Number(selected) - 1],
            });
            //let user know it worked
            setLoginModal(false);
            return response.status;
        } catch (error) {
            //user is not logged in
        }
        setLoginModal(false);
    };

    return (
        <>
            <Button className="btn-round" color="danger" type="button" onClick={() => setLoginModal(true)} style={{ height: "30px", paddingTop: "2%", marginTop: "10%" }}>
                <BsFillExclamationCircleFill /> Report
            </Button>
            <Modal isOpen={loginModal} toggle={() => setLoginModal(false)} modalClassName="modal-register">
                <div className="modal-header no-border-header text-center" id="reportComment">
                    <button aria-label="Close" className="close" data-dismiss="modal" type="button" onClick={() => setLoginModal(false)}>
                        <span aria-hidden={true}>×</span>
                    </button>
                    <h3 className="modal-title text-center">Report this comment?</h3>
                </div>
                <div className="modal-body" id="reportComment">
                    <FormGroup tag="fieldset">
                        <legend>What is wrong with this comment?</legend>
                        <FormGroup check>
                            <Label check>
                                <Input type="radio" onClick={handlePress} id="1" name="radio1" /> It contains offensive content
                            </Label>
                        </FormGroup>
                        <FormGroup check>
                            <Label check>
                                <Input type="radio" id="2" onClick={handlePress} name="radio1" /> It is clearly untrue
                            </Label>
                        </FormGroup>
                        <FormGroup check>
                            <Label check>
                                <Input type="radio" onClick={handlePress} id="3" name="radio1" /> Does not contain relevant information to this review
                            </Label>
                        </FormGroup>
                        <FormGroup check>
                            <Label check>
                                <Input type="radio" onClick={handlePress} id="4" name="radio1" /> Other. (Let us know why below)
                            </Label>
                        </FormGroup>
                        <FormGroup>
                            <Input type="textarea" onChange={handleChange} name="content" id="content" rows={3} />
                        </FormGroup>
                    </FormGroup>
                    <Button block className="btn-round" onClick={submit} color="default">
                        Report
                    </Button>
                </div>
            </Modal>
        </>
    );
}

export default ReportCommentForm;
